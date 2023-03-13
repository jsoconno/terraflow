import json
from pathlib import Path
import subprocess
import requests
from bs4 import BeautifulSoup
import re
import os
import difflib
import errno

from terraflow.libraries.constants import *

def colors(color="END"):
    """
    A standard set of colors used for printing to command line.
    """
    colors = {
        "HEADER": "\033[95m",
        "OK_BLUE": "\033[94m",
        "OK_CYAN": "\033[96m",
        "OK_GREEN": "\033[92m",
        "WARNING": "\033[93m",
        "FAIL": "\033[91m",
        "END": "\033[0m",
        "BOLD": "\033[1m",
        "UNDERLINE": "\033[4m",
    }

    return colors[color]

def get_schema(
    namespace="hashicorp",
    provider=None,
    scope="resource",
    resource=None,
    attribute=None,
    blocks=None,
    filename=None
):
    """
    Returns the schema for a provider as a dictionary.
    """
    # Get the full schema
    if filename:
        with open(filename, "r") as schema:
            schema = json.loads(schema.read())
    else:
        try:
            schema = json.loads(
                subprocess.check_output(
                    ["terraform", "providers", "schema", "-json"]
                ).decode("utf-8")
            )
        except:
            subprocess.run(
                ["terraform", "init", "-upgrade"], capture_output=True, text=True
            )
            schema = json.loads(
                subprocess.check_output(
                    ["terraform", "providers", "schema", "-json"]
                ).decode("utf-8")
            )

    # Get scope schema
    if namespace and provider:
        if scope in ALLOWED_SCOPES:
            if scope == "provider":
                schema = schema["provider_schemas"][
                    f"registry.terraform.io/{namespace}/{provider}"
                ][scope]
            elif scope == "resource" or scope == "data_source":
                schema = schema["provider_schemas"][
                    f"registry.terraform.io/{namespace}/{provider}"
                ][f"{scope}_schemas"][resource]
        else:
            schema = schema["provider_schemas"][
                f"registry.terraform.io/{namespace}/{provider}"
            ]

    # Get the attribute schema
    if attribute:
        if blocks:
            # Loop over all blocks in the blocks list
            for block in blocks:
                # Go down into blocks until desired block is found
                schema = schema["block"]["block_types"].get(block, None)

        schema = schema["block"]["attributes"].get(attribute, None)

    return schema


def list_items(schema, namespace="hashicorp", provider=None, scope="resource"):
    """
    Returns an available list of providers based on the configuration.
    """
    items = []

    try:
        if scope in ALLOWED_SCOPES:
            if scope == "provider":
                schema = schema[f"provider_schemas"]
                for provider in schema:
                    provider = provider.replace("registry.terraform.io/", "").split(
                        "/"
                    )[1]
                    items.append(provider)
            else:
                schema = schema["provider_schemas"][
                    f"registry.terraform.io/{namespace}/{provider}"
                ][f"{scope}_schemas"]
                for source in schema:
                    items.append(source)
        else:
            print(f"The scope must be one of {ALLOWED_SCOPES}.")
    except:
        print("No items were found.")

    return items


def download_schema(schema, filename='schema'):
    # Set a default filename
    if filename == None:
        filename = 'schema'

    # Create file
    with open(f"{filename}.json", "w+") as f:
        f.write(json.dumps(schema))


def write_to_file(text, filename, regex_pattern=None, overwrite=False):
    try:
        with open(filename, 'r+') as f:
            # Read the file contents
            contents = f.read()
            if not contents.endswith('\n'):
                contents += '\n\n'
    except:
        contents = ''
        
    with open(filename, 'w+') as f:
        # If the pattern matches, append or overwrite the text
        if overwrite:
            if contents != '':
                if re.search(regex_pattern, contents, flags=re.MULTILINE):
                    current_text = re.findall(pattern=regex_pattern, string=contents, flags=re.MULTILINE)[0]
                    text = contents.replace(current_text, text)
                else:
                    text = contents + text
            else:
                text = contents + text
        
        f.write(text.strip())


def get_attribute_value(attribute_schema, attribute):
    """
    Returns the schema for a resource attribute as a dictionary.
    """
    if attribute in ALLOWED_ATTRIBUTES:
        value = attribute_schema.get(attribute, None)
    else:
        print(f"The attribute must be one of {ALLOWED_ATTRIBUTES}.")

    return value


def format_attribute_type(attribute_type):
    """
    Formats the data type for terraform variables.
    """
    if isinstance(attribute_type, str):
        return attribute_type
    elif isinstance(attribute_type, list):
        element_type = format_attribute_type(attribute_type[-1])
        for i in range(len(attribute_type) - 2, -1, -1):
            element_type = f"{attribute_type[i]}({element_type})"
        return element_type
    elif isinstance(attribute_type, dict):
        object_type = ""
        for key, value in attribute_type.items():
            object_type += f"{key} = {format_attribute_type(value)}\n"
        return object_type
    else:
        raise ValueError(f"Invalid Terraform data type: {attribute_type}")


def set_attribute_value(
    block_list, attribute_name, attribute_value_prefix=None, attribute_defaults={}
):
    """
    Creates an attributes variable name based on the nesting of blocks and attributes name with an optional prefix.
    """
    # Add the variable prefix, if one is provided
    if attribute_value_prefix:
        attribute_value = "_".join(
            [attribute_value_prefix] + block_list + [attribute_name]
        )
    # Otherwise, simply join the block list to the attribute_name
    else:
        attribute_value = "_".join(block_list + [attribute_name])

    # Set the attribute default
    attribute_default = attribute_defaults.get(attribute_name, None)

    # If an attribute default is set for the attribute
    if attribute_default:
        # If there is a period in the default value
        if "." in attribute_default:
            # Set the value without quotes for things like resource_type.name.attribute
            attribute_value = attribute_default
        else:
            # Otherwise, set as a string with quotes
            attribute_value = f'"{attribute_default}"'
    else:
        # Otherwise, set as a variable using the nested attribute value
        attribute_value = f"var.{attribute_value}"

    return attribute_value


def is_required_attribute(attribute_schema):
    """
    Determines whether or not an attribute is required.
    """
    # Set the default to None
    attribute_required = None

    # Determine if an attribute is required or optional
    if not 'computed' in attribute_schema:
        if "required" in attribute_schema:
            attribute_required = True
        elif "optional" in attribute_schema:
            attribute_required = False

    return attribute_required


def is_required_block(block_min_items):
    if block_min_items:
        block_required = True
    else:
        block_required = False

    return block_required


def recurse_schema(
    schema={},
    level=0,
    current_block="root",
    block_list=[],
    total_blocks=0,
    current_block_number=0,
    documentation_text='',
    scope=None,
    namespace='hashicorp',
    provider=None,
    resource=None,
    required_attributes_only=False,
    required_blocks_only=False,
    add_descriptions=False,
    ignore_blocks=[],
    ignore_attributes=[],
    attribute_defaults={},
    attribute_value_prefix=None,
):
    # Set defaults
    lines = []

    # Determine what the attribute and block schema should be
    if current_block == "root":
        attributes = schema.get("block").get("attributes", None)
        blocks = schema.get("block").get("block_types", None)
        # Collect the documentation
        if add_descriptions:
            documentation_text = get_resource_documentation(
                namespace=namespace,
                provider=provider,
                resource=resource
            )
    else:
        attributes = schema.get("block").get("attributes", None)
        blocks = schema.get("block").get("block_types", None)

    # If there are attributes in a schema
    if attributes:
        # Increase the indent by one level
        level += 1
        # Add the current block to block list if not at the root
        if current_block != "root":
            block_list.append(current_block)
        # Loop through all attributes
        for attribute, attribute_schema in attributes.items():
            # Add the current block to the block chain if not root
            # To help keep track of naming for variables and hierarchy
            line = f'{level * "  "}{attribute} = var.{attribute}'

            # Determine if the attribute is required
            attribute_required = is_required_attribute(
                attribute_schema=attribute_schema
            )

            # Skip attributes
            if required_attributes_only or "_".join(block_list + [attribute]) in ignore_attributes or attribute_required == None:
                if not attribute_required:
                    continue

            # Get the value that should be set for the attribute
            attribute_value = set_attribute_value(
                block_list=block_list,
                attribute_name=attribute,
                attribute_value_prefix=attribute_value_prefix,
                attribute_defaults=attribute_defaults,
            )

            # Set attribute description
            attribute_description = get_attribute_value(
                attribute_schema=attribute_schema, attribute="description"
            )

            # if attribute == 'location':
            #     print('stop')

            if attribute_description == None and documentation_text:
                try:
                    attribute_description = get_resource_attribute_description(
                        documentation_text=documentation_text,
                        attribute=attribute,
                        block_list=block_list
                    )
                except Exception as e:
                    print(e)
                    attribute_description = ''

            # Write attributes based on whether or not they are required
            if attribute_required:
                line = f'{level * "  "}{attribute} = {attribute_value}'
            elif not attribute_required and not required_attributes_only:
                line = f'{level * "  "}{attribute} = {attribute_value}'

            if attribute_description and add_descriptions:
                line = f"{line} # {attribute_description}"

            lines.append(line)

    # If there are blocks in the schema
    if blocks:
        # Set the current block number to 0
        current_block_number = 0
        # Loop through all blocks
        for block, schema in blocks.items():
            # Set min and max items for block
            block_min_items = schema.get("min_items", None)
            block_max_items = schema.get("max_items", None)

            # Determine if the block is required
            block_required = is_required_block(block_min_items=block_min_items)

            # Skip blocks
            if required_blocks_only or block in ignore_blocks or block_required == None:
                if not block_required:
                    continue

            # Determine if multiple blocks are allowed
            if block_max_items and block_max_items > 1:
                multiple_blocks_allowed = True
            else:
                multiple_blocks_allowed = False

            # Write a comment describing the constraints of the block
            if block_required:
                if multiple_blocks_allowed:
                    lines.append(
                        f'\n{level * "  "}# This block is required and allows for up to {block_max_items} items.'
                    )
                else:
                    lines.append(
                        f'\n{level * "  "}# This block is required and allows only one item.'
                    )
            else:
                if multiple_blocks_allowed:
                    lines.append(
                        f'\n{level * "  "}# This block is optional and allows for up to {block_max_items} items.'
                    )
                else:
                    lines.append(
                        f'\n{level * "  "}# This block is optional and allows only one item.'
                    )

            # Increment the block number
            current_block_number += 1
            # Calculate the total blocks
            total_blocks = len(blocks)
            # Add line for the start of the block resource
            lines.append(f'{level * "  "}{block} {{')
            # Get the lines for the attributes that go into the block
            child_lines = recurse_schema(
                schema=schema,
                level=level,
                current_block=block,
                block_list=block_list,
                total_blocks=total_blocks,
                current_block_number=current_block_number,
                documentation_text=documentation_text,
                scope=scope,
                namespace=namespace,
                provider=provider,
                resource=resource,
                required_attributes_only=required_attributes_only,
                required_blocks_only=required_blocks_only,
                add_descriptions=add_descriptions,
                ignore_attributes=ignore_attributes,
                ignore_blocks=ignore_blocks,
                attribute_defaults=attribute_defaults,
                attribute_value_prefix=attribute_value_prefix,
            )
            # Add the lines to the block
            lines.extend(child_lines)
            # Remove the last item in the block list
            del block_list[-1:]

        # Reset block list for new blocks
        block_list = []

    # Reduce indent by one level
    level = level - 1
    # Write the closing bracket for the block
    line = f'{level * "  "}}}'
    # Append the line to the list
    lines.append(line)

    return lines


def write_code(
    schema,
    scope=None,
    namespace='hashicorp',
    provider=None,
    resource=None,
    resource_name="main",
    required_attributes_only=False,
    required_blocks_only=False,
    add_descriptions=False,
    ignore_blocks=[],
    ignore_attributes=[],
    attribute_defaults={},
    attribute_value_prefix=None,
    configuration_file="main.tf",
    output_code=True,
    overwrite_code=True,
    format_code=True,
):
    code_lines = []

    if scope in ALLOWED_SCOPES:
        if scope == "provider":
            if provider:
                header = f'provider "{provider}" {{'
            else:
                print(f"A {scope} must be specified when the scope is set to {scope}.")
        else:
            if resource:
                header = f'{scope.split("_")[0]} "{resource}" "{resource_name}" {{'
            else:
                print(
                    f'A {scope.replace("_", " ")} must be specified when the scope is set to {scope}.'
                )
    else:
        print(f"The scope must be one of {ALLOWED_SCOPES}.")

    body = recurse_schema(
        schema=schema,
        scope=scope,
        namespace=namespace,
        provider=provider,
        resource=resource,
        required_attributes_only=required_attributes_only,
        required_blocks_only=required_blocks_only,
        add_descriptions=add_descriptions,
        ignore_attributes=ignore_attributes,
        ignore_blocks=ignore_blocks,
        attribute_defaults=attribute_defaults,
        attribute_value_prefix=attribute_value_prefix,
    )

    code_lines.append(header)
    code_lines.extend(body)

    # Combine all lines into one text document
    code = "\n".join(code_lines)

    # If the user wants the code to be written to file:
    if output_code == True:
        # Write file
        write_to_file(
            text=code,
            filename=configuration_file,
            regex_pattern=rf'^resource\s+"{resource}"\s+"{resource_name}"\s+{{[\s\S]*?^}}$',
            overwrite=overwrite_code
        )

        # Format code
        if format_code:
            p = subprocess.run(["terraform", "fmt"])

    return code

def levenshtein_distance(s, t):
    # Convert the strings to lowercase
    s = s.lower()
    t = t.lower()

    # Initialize the distance matrix with zeros
    d = [[0 for j in range(len(t) + 1)] for i in range(len(s) + 1)]

    # Fill the first row and column of the matrix
    for i in range(len(s) + 1):
        d[i][0] = i
    for j in range(len(t) + 1):
        d[0][j] = j

    # Compute the minimum edit distance
    for j in range(1, len(t) + 1):
        for i in range(1, len(s) + 1):
            if s[i - 1] == t[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1]) + 1

    # Compute the maximum possible distance
    max_distance = max(len(s), len(t))

    # Normalize the distance
    if max_distance == 0:
        normalized_distance = 0.0
    else:
        normalized_distance = d[len(s)][len(t)] / max_distance

    return normalized_distance

def get_resource_documentation(namespace, provider, resource, scope='resource'):
    url = f'https://registry.terraform.io/v1/providers/{namespace}/{provider}'
    response = json.loads(requests.get(url).text)

    docs_path = None
    
    for doc in response["docs"]:
        if doc["title"] == resource or doc["title"] == resource.replace(f'{provider}_', '') and doc["category"] == f'{scope}s':
            docs_path = doc["path"]

    if docs_path:
        docs_url = f'https://github.com/{namespace}/terraform-provider-{provider}/blob/main/{docs_path}'

        html_text = requests.get(docs_url).content.decode()
        soup = BeautifulSoup(html_text, features="html.parser")

        # Extract the text from the HTML document while preserving special characters
        documentation = re.sub(r'<[^>]*>', '', soup.text)  # Remove all HTML tags
        documentation = re.sub(r'(\n\s*)+', '\n', documentation)  # Normalize newlines
        documentation = documentation.strip()
    else:
        print('Documentation not found.')
        documentation = None

    return documentation

def get_resource_attribute_description(documentation_text, attribute, block_list=None):
    # Extract the attribute descriptions from the text
    pattern = rf'(^{attribute})\s+-\s+(.*)'
    attribute_matches = re.findall(pattern=pattern, string=documentation_text, flags=re.MULTILINE)
    attribute_matches = [str(x[1]) for x in attribute_matches]

    # print("_".join(block_list + [attribute]))
        
    # if there is more than one match on an attribute name
    if len(attribute_matches) > 1:
        # Check is there is a list of blocks
        if block_list:
            # Then for each match rank them based on a normalized distance algorithm
            levenshtein_distances = []
            for match in attribute_matches:
                normalized_block_text = " ".join(block_list).replace("_", " ")
                # Calculate the normalized distance
                normalized_distance = levenshtein_distance(match, normalized_block_text)
                current_block = block_list[-1]
                # If the current block name is in the match
                if current_block in match:
                    # Add a multiplier if the exact block name is in the string
                    normalized_distance = normalized_distance - .1
                else:
                    # For each key word in the block list
                    for keyword in block_list:
                        # Go through each word in the description text
                        for word in match.split(' '):
                            # Calculate a similarity score
                            similarity_score = difflib.SequenceMatcher(None, keyword.lower().replace('_', ' '), word.lower()).ratio()
                            # And if that score is below a threshold, add another multiplier
                            if similarity_score > .8:
                                # print(f'{keyword} -> {word} = score: {similarity_score}')
                                normalized_distance = normalized_distance - .1
                        # elif word 
                # Create a list of scores
                levenshtein_distances.append(normalized_distance)

            # Sort and get the lowest scoring description
            levenshtein_distances, descriptions = zip(*sorted(zip(levenshtein_distances, attribute_matches)))

            # Select the description with the lowest distance
            description = descriptions[0]

            # print(levenshtein_distances)
            # print(descriptions)
        else:
            description = ''
    else:
        description = attribute_matches[0]

    return description

# description = get_resource_attribute_description(
#     namespace='hashicorp',
#     provider='azurerm',
#     resource='azurerm_linux_function_app',
#     attribute='login_scopes',
#     scope='resource',
#     block_list=['google_v2']
# )

# print(description)

def convert_strings_to_dict(text, delimiter='='):
    
    dictionary = {}
    for x in text:
        k, v = x.split(delimiter)
        dictionary[k] = v

    return dictionary