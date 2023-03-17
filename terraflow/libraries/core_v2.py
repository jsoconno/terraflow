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
    # Determine if there is an existing schema file locally
    if filename == None and os.path.exists('schema.json'):
        filename = 'schema.json'
    
    # Get the full schema
    if filename:
        with open(filename, "r") as schema:
            schema = json.loads(schema.read())
    else:
        try:
            subprocess.run(
                ["terraform", "init"], capture_output=True, text=True
            )
            schema = json.loads(
                subprocess.check_output(
                    ["terraform", "providers", "schema", "-json"]
                ).decode("utf-8")
            )
            print(f'\n{colors("OK_GREEN")}Success:{colors()} The schema was downloaded successfully.\n')
        except:
            print(f'\n{colors("WARNING")}Warning:{colors()} The dependency lock file does not match the current configuration.  Running terraform init -upgrade to collect the latest schema for the selected provider versions.\n')
            subprocess.run(
                ["terraform", "init", "-upgrade"], capture_output=True, text=True
            )
            schema = json.loads(
                subprocess.check_output(
                    ["terraform", "providers", "schema", "-json"]
                ).decode("utf-8")
            )
            print(f'\n{colors("OK_GREEN")}Success:{colors()} The schema was downloaded successfully.\n')

    # Get scope schema
    if namespace and provider:
        if scope in ALLOWED_SCOPES:
            if scope == "provider":
                schema = schema["provider_schemas"][
                    f"registry.terraform.io/{namespace}/{provider}"
                ][scope]
            elif scope == "resource" or scope == "data_source":
                # Allow resource shorthand without the provider
                if resource and not provider in resource:
                    resource = f'{provider}_{resource}'
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

def write_to_file(text, filename, regex_pattern=None):
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
        if contents != '':
            if re.search(regex_pattern, contents, flags=re.MULTILINE):
                current_text = re.findall(pattern=regex_pattern, string=contents, flags=re.MULTILINE)[0]
                text = contents.replace(current_text, text)
            else:
                text = contents + text
        else:
            text = contents + text
        
        f.write(text.strip())

# def get_attribute_value(attribute_schema, attribute):
#     """
#     Returns the schema for a resource attribute as a dictionary.
#     """
#     if attribute in ALLOWED_ATTRIBUTES:
#         value = attribute_schema.get(attribute, None)
#     else:
#         print(f"The attribute must be one of {ALLOWED_ATTRIBUTES}.")

#     return value


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
        object_type = "{\n"
        for key, value in attribute_type.items():
            object_type += f"{key} = {format_attribute_type(value)}\n"
        object_type += "}"
        return object_type
    else:
        raise ValueError(f"Invalid Terraform data type: {attribute_type}")


def set_attribute_value(
    attribute, block_hierarchy, attribute_value_prefix=None, attribute_defaults={}
):
    """
    Creates an attributes variable name based on the nesting of blocks and attributes name with an optional prefix.
    """
    # Add the variable prefix, if one is provided
    if attribute_value_prefix:
        attribute_value = "_".join(
            [attribute_value_prefix] + block_hierarchy + [attribute]
        )
    # Otherwise, simply join the block list to the attribute_name
    else:
        attribute_value = "_".join(block_hierarchy + [attribute])

    # Set the attribute default
    attribute_default = attribute_defaults.get(attribute_value, None)

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

def get_resource_attribute_description(documentation_text, attribute, block_hierarchy=None):
    # Extract the attribute descriptions from the text
    pattern = rf'(^{attribute})\s+-\s+(.*)'
    attribute_matches = re.findall(pattern=pattern, string=documentation_text, flags=re.MULTILINE)
    attribute_matches = [str(x[1]) for x in attribute_matches]
        
    # if there is more than one match on an attribute name
    if len(attribute_matches) > 1:
        # Check is there is a list of blocks
        if block_hierarchy:
            # Then for each match rank them based on a normalized distance algorithm
            levenshtein_distances = []
            for match in attribute_matches:
                normalized_block_text = " ".join(block_hierarchy).replace("_", " ")
                # Calculate the normalized distance
                normalized_distance = levenshtein_distance(match, normalized_block_text)
                current_block = block_hierarchy[-1]
                # If the current block name is in the match
                if current_block in match:
                    # Add a multiplier if the exact block name is in the string
                    normalized_distance = normalized_distance - .1
                else:
                    # For each key word in the block list
                    for keyword in block_hierarchy:
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
            # Take the first item found
            description = attribute_matches[0]
    elif len(attribute_matches) == 1:
        description = attribute_matches[0]
    else:
        description = ''


    return description

def convert_strings_to_dict(text, delimiter='='):
    
    dictionary = {}
    for x in text:
        k, v = x.split(delimiter)
        dictionary[k] = v

    return dictionary

def recurse_schema(
    schema,
    func,
    add_descriptions=False,
    ignore_attributes=[],
    ignore_blocks=[],
    required_attributes_only=False,
    required_blocks_only=False,
    *args,
    **kwargs
):
    # Start with an empty list for the lines of code and block hierarchy
    lines = []
    block_hierarchy = []

    # Collect the documentation
    if add_descriptions and not kwargs['resource'] == None:
        documentation_text = get_resource_documentation(
            namespace=kwargs['namespace'],
            provider=kwargs['provider'],
            resource=kwargs['resource']
        )
    else:
        documentation_text = None
    
    # Get the attributes and blocks from the schema
    attributes = schema.get("block", {}).get("attributes", {})
    blocks = schema.get("block", {}).get("block_types", {})

    # Call the function on each attribute
    for attribute, attribute_schema in attributes.items():
        # Determine if the attribute is required
        required_attribute = is_required_attribute(
            attribute_schema=attribute_schema
        )
        if required_attributes_only or "_".join(kwargs['block_hierarchy'] + [attribute]) in ignore_attributes or required_attribute == None and not required_attribute:
            continue
        else:
            result = func(attribute=attribute, attribute_schema=attribute_schema, documentation_text=documentation_text, **kwargs)
            if result is not None:
                lines.append(result)

    # Recursively call this function on each block
    for block, block_schema in blocks.items():
        # Set min and max items for block
        block_min_items = schema.get("min_items", None)
        block_max_items = schema.get("max_items", None)

        # Determine if the block is required
        required_block = is_required_block(block_min_items=block_min_items)

        # Skip blocks
        if required_blocks_only or "_".join(kwargs['block_hierarchy'] + [block]) in ignore_blocks or required_block == None and not required_block:
            continue
        else:
            block_hierarchy.append(block)
            block_lines = recurse_schema(schema=block_schema, func=func, add_descriptions=add_descriptions, *args, **kwargs)
            lines.append(f"{block} {{")
            lines.extend([f"  {line}" for line in block_lines])
            lines.append("}")
            del block_hierarchy[-1:]

    return lines

def generate_config_code(attribute, attribute_schema, documentation_text, **kwargs):

    # line_of_code = f'{attribute} = var.{"_".join(block_hierarchy + [attribute])}'
    # print(kwargs)
    line_of_code = write_attribute(
        attribute=attribute,
        attribute_schema=attribute_schema,
        documentation_text=documentation_text,
        block_hierarchy=kwargs['block_hierarchy'],
        attribute_value_prefix=kwargs['attribute_value_prefix'],
        attribute_defaults=kwargs['attribute_defaults']
    )

    return line_of_code

def write_attribute(attribute, attribute_schema, documentation_text, **kwargs):
    # Get the value that should be set for the attribute
    attribute_value = set_attribute_value(
        attribute=attribute,
        block_hierarchy=kwargs['block_hierarchy'],
        attribute_value_prefix=kwargs['attribute_value_prefix'],
        attribute_defaults=kwargs['attribute_defaults']
    )

    # Get the attribute description if the user providers documentation text
    if documentation_text:
        try:
            attribute_description = get_resource_attribute_description(
                documentation_text=documentation_text,
                attribute=attribute,
                block_hierarchy=kwargs['block_hierarchy']
            )
        except Exception as e:
            attribute_description = get_attribute_value(
                attribute_schema=attribute_schema, attribute='description'
            )
        finally:
            attribute_description = attribute_description.replace('"', "'")
    else:
        attribute_description = None

    if attribute_description:
        line_of_code = f'{attribute} = {attribute_value} # {attribute_description}'
    else:
        line_of_code = f'{attribute} = {attribute_value}'

    return line_of_code

def write_provider_code(
    provider,
    namespace='hashicorp',
    ignore_attributes=[],
    ignore_blocks=[],
    required_attributes_only=False,
    required_blocks_only=False,
    add_descriptions=False,
    attribute_defaults={},
    attribute_value_prefix='',
    filename='providers.tf',
    schema_filename=None,
):
    schema = get_schema(
        namespace=namespace,
        provider=provider,
        scope='provider',
        filename=schema_filename
    )

    header = f'provider "{provider}" {{'
    regex_pattern = rf'^provider\s+"{provider}"\s+{{[\s\S]*?^}}$'

    body = recurse_schema(
        schema=schema,
        func=generate_config_code,
        add_descriptions=add_descriptions,
        namespace=namespace,
        provider=provider,
        block_hierarchy=[],
        ignore_attributes=ignore_attributes,
        ignore_blocks=ignore_blocks,
        required_attributes_only=required_attributes_only,
        required_blocks_only=required_blocks_only,
        attribute_value_prefix=attribute_value_prefix,
        attribute_defaults=attribute_defaults
    )

    footer = '}'

    # Combine all code lists
    code = [header] + body + [footer]

     # Turn the code list into text
    code = "\n".join(code)

    # Write file
    write_to_file(
        text=code,
        filename=filename,
        regex_pattern=regex_pattern
    )

    # Format code
    subprocess.run(["terraform", "fmt"])

    return code

def write_resource_code(
    provider,
    resource,
    namespace='hashicorp',
    ignore_attributes=[],
    ignore_blocks=[],
    required_attributes_only=False,
    required_blocks_only=False,
    add_descriptions=False,
    attribute_defaults={},
    attribute_value_prefix='',
    filename='main.tf',
    name='main',
    schema_filename=None,
):
    schema = get_schema(
        namespace=namespace,
        provider=provider,
        resource=resource,
        scope='resource',
        filename=schema_filename
    )

    header = f'resource "{resource}" "{name}" {{'
    regex_pattern = rf'^resource\s+"{resource}"\s+"{name}"\s+{{[\s\S]*?^}}$'

    body = recurse_schema(
        schema=schema,
        func=generate_config_code,
        add_descriptions=add_descriptions,
        namespace=namespace,
        provider=provider,
        resource=resource,
        block_hierarchy=[],
        ignore_attributes=ignore_attributes,
        ignore_blocks=ignore_blocks,
        required_attributes_only=required_attributes_only,
        required_blocks_only=required_blocks_only,
        attribute_value_prefix=attribute_value_prefix,
        attribute_defaults=attribute_defaults
    )

    footer = '}'

    # Combine all code lists
    code = [header] + body + [footer]

     # Turn the code list into text
    code = "\n".join(code)

    # Write file
    write_to_file(
        text=code,
        filename=filename,
        regex_pattern=regex_pattern
    )

    # Format code
    subprocess.run(["terraform", "fmt"])

    return code

def write_data_source_code(
    provider,
    resource,
    namespace='hashicorp',
    ignore_attributes=[],
    ignore_blocks=[],
    required_attributes_only=False,
    required_blocks_only=False,
    add_descriptions=False,
    attribute_defaults={},
    attribute_value_prefix='',
    filename='data-sources.tf',
    name='main',
    schema_filename=None,
):
    schema = get_schema(
        namespace=namespace,
        provider=provider,
        resource=resource,
        scope='data_source',
        filename=schema_filename
    )

    header = f'data "{resource}" "{name}" {{'
    regex_pattern = rf'^data\s+"{resource}"\s+"{name}"\s+{{[\s\S]*?^}}$'

    body = recurse_schema(
        schema=schema,
        func=generate_config_code,
        add_descriptions=add_descriptions,
        namespace=namespace,
        provider=provider,
        resource=resource,
        block_hierarchy=[],
        ignore_attributes=ignore_attributes,
        ignore_blocks=ignore_blocks,
        required_attributes_only=required_attributes_only,
        required_blocks_only=required_blocks_only,
        attribute_value_prefix=attribute_value_prefix,
        attribute_defaults=attribute_defaults
    )

    footer = '}'

    # Combine all code lists
    code = [header] + body + [footer]

     # Turn the code list into text
    code = "\n".join(code)

    # Write file
    write_to_file(
        text=code,
        filename=filename,
        regex_pattern=regex_pattern
    )

    # Format code
    subprocess.run(["terraform", "fmt"])

    return code

# code = write_data_source_code(
#     provider='azurerm',
#     resource='key_vault',
#     add_descriptions=True
# )