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
    filename=None,
):
    """
    Returns the schema for a provider as a dictionary.
    """
    # Get the schema from file
    if filename and os.path.exists(filename):
        with open(filename, "r") as schema:
            schema = json.loads(schema.read())
    else:
        try:
            p = subprocess.run(["terraform", "init"], capture_output=True, text=True)
            schema = json.loads(
                subprocess.check_output(
                    ["terraform", "providers", "schema", "-json"]
                ).decode("utf-8")
            )
        except subprocess.CalledProcessError:
            print(
                f'\n{colors(color="WARNING")}Warning:{colors()} The provider versions for this configuration have changed.  Running an upgrade.\n'
            )
            p = subprocess.run(
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
                # Allow resource shorthand without the provider
                if resource and not provider in resource:
                    resource = f"{provider}_{resource}"
                try:
                    schema = schema["provider_schemas"][
                        f"registry.terraform.io/{namespace}/{provider}"
                    ][f"{scope}_schemas"][resource]
                except Exception as e:
                    print(
                        f'{colors(color="WARNING")}\nThe value {str(e)} is invalid.  Did you mean {resource.replace("-", "_").replace(provider + "_", "")}?\n{colors()}'
                    )
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


def download_schema(filename="schema.json", refresh=False):
    # Check if the file type is .json
    if not filename.endswith(".json"):
        print(f'\n{colors("FAIL")}Error:{colors()} {filename} is not a json file.\n')
        return

    # Determine if there is an existing schema file locally
    if os.path.exists(filename) and not refresh:
        # If the file exists and refresh is False, exit the function
        print(
            f'\n{colors("OK_BLUE")}Tip:{colors()} A schema is already downloaded.  To refresh the schema, rerun this command with the `--refresh` flag.\n'
        )
        return
    else:
        # If the file doesn't exist or refresh is True, call get_schema()
        schema = get_schema()

        # Create or overwrite the file
        with open(filename, "w") as f:
            f.write(json.dumps(schema))

        print(
            f'\n{colors("OK_GREEN")}Success:{colors()} Schema downloaded successfully.\n'
        )


def write_to_file(text, filename, regex_pattern=None):
    try:
        with open(filename, "r+") as f:
            # Read the file contents
            contents = f.read()
    except:
        contents = ""

    with open(filename, "w+") as f:
        # If the pattern matches, append or overwrite the text
        if contents != "":
            if not contents.endswith("\n"):
                contents += "\n\n"
            if re.search(regex_pattern, contents, flags=re.MULTILINE):
                current_text = re.findall(
                    pattern=regex_pattern, string=contents, flags=re.MULTILINE
                )[0]
                text = contents.replace(current_text, text)
            else:
                text = contents + text
        else:
            text = contents + text

        f.write(text.strip())


def list_items(
    schema, namespace="hashicorp", provider=None, scope="resource", keywords=None
):
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
                    items.append(source.replace(f"{provider}_", ""))
        else:
            print(f"The scope must be one of {ALLOWED_SCOPES}.")
    except:
        print("No items were found.")

    if keywords:
        items = [item for item in items if any(keyword in item for keyword in keywords)]

    return items


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
    attribute,
    block_hierarchy,
    attribute_value_prefix=None,
    attribute_defaults={},
    dynamic_blocks=[],
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
        if dynamic_blocks and block_hierarchy:
            if "_".join(block_hierarchy) in dynamic_blocks:
                attribute_value = f'{"_".join(block_hierarchy)}.value["{attribute}"]'
            elif all(elem in block_hierarchy for elem in dynamic_blocks):
                x = "_".join(block_hierarchy[1:])
                attribute_value = (
                    f'{block_hierarchy[0]}.value["{x + "_" if x else x}{attribute}"]'
                )
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
    if not "computed" in attribute_schema:
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


def get_resource_documentation_url(namespace, provider, resource, scope, version='main'):
    url = f"https://registry.terraform.io/v1/providers/{namespace}/{provider}"
    response = json.loads(requests.get(url).text)

    docs_path = None

    for doc in response["docs"]:
        if (
            doc["title"] == resource
            or doc["title"] == resource.replace(f"{provider}_", "")
            and doc["category"] == f"{scope.replace('_', '-')}s"
        ):
            docs_path = doc["path"]

    if docs_path:
        if scope == "provider":
            url = f"https://github.com/{namespace}/terraform-provider-{provider}"
        else:
            # TODO: replace "main" with the actual version of the provider from the configuration.
            url = f"https://github.com/{namespace}/terraform-provider-{provider}/blob/{version}/{docs_path}"
    else:
        url = None

    return url


def get_resource_documentation(documentation_url):
    if documentation_url:
        html_text = requests.get(documentation_url).content.decode()
        soup = BeautifulSoup(html_text, features="html.parser")

        # Extract the text from the HTML document while preserving special characters
        documentation = re.sub(r"<[^>]*>", "", soup.text)  # Remove all HTML tags
        documentation = re.sub(r"(\n\s*)+", "\n", documentation)  # Normalize newlines
        documentation = documentation.strip()
    else:
        print(f'\n{colors(color="WARNING")}Warning:{colors()}\n')
        documentation = None

    return documentation


def get_resource_attribute_description(
    documentation_text, attribute, block_hierarchy=None
):
    # Extract the attribute descriptions from the text
    pattern = rf"(^{attribute})\s+-\s+(.*)"
    attribute_matches = re.findall(
        pattern=pattern, string=documentation_text, flags=re.MULTILINE
    )
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
                    normalized_distance = normalized_distance - 0.1
                else:
                    # For each key word in the block list
                    for keyword in block_hierarchy:
                        # Go through each word in the description text
                        for word in match.split(" "):
                            # Calculate a similarity score
                            similarity_score = difflib.SequenceMatcher(
                                None, keyword.lower().replace("_", " "), word.lower()
                            ).ratio()
                            # And if that score is below a threshold, add another multiplier
                            if similarity_score > 0.8:
                                # print(f'{keyword} -> {word} = score: {similarity_score}')
                                normalized_distance = normalized_distance - 0.1
                        # elif word
                # Create a list of scores
                levenshtein_distances.append(normalized_distance)

            # Sort and get the lowest scoring description
            levenshtein_distances, descriptions = zip(
                *sorted(zip(levenshtein_distances, attribute_matches))
            )

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
        description = ""

    return description


def convert_strings_to_dict(text, delimiter="="):
    dictionary = {}
    for x in text:
        k, v = x.split(delimiter)
        dictionary[k] = v

    return dictionary


def write_attribute(
    attribute,
    attribute_schema,
    block_hierarchy,
    attribute_value_prefix,
    attribute_defaults,
    dynamic_blocks,
    documentation_text=None,
    add_descriptions=False
):
    # Get the value that should be set for the attribute
    attribute_value = set_attribute_value(
        attribute=attribute,
        block_hierarchy=block_hierarchy,
        attribute_value_prefix=attribute_value_prefix,
        attribute_defaults=attribute_defaults,
        dynamic_blocks=dynamic_blocks,
    )
    # Get the attribute's description
    description = ""

    if add_descriptions:
        if documentation_text:
            # Attempt to get the description from the documentation_text
            description = get_resource_attribute_description(
                documentation_text=documentation_text,
                attribute=attribute,
                block_hierarchy=block_hierarchy,
            )
        
        if not description:
            # Attempt to get the description from the attribute_schema
            description = attribute_schema.get("description", "")

    # Clean up text so that only single quotes are used in descriptions
    description = description.replace('"', "'")

    if description:
        line_of_code = f"{attribute} = {attribute_value} # {description}"
    else:
        line_of_code = f"{attribute} = {attribute_value}"

    return line_of_code


def pretty_list(items=[], title=None, top=None, item_prefix=" - "):
    """
    Implements logic to make output to CLI more clean and consistent.
    """
    pretty_list = "\n"

    if isinstance(items, str):
        items = [items]

    if len(items) > 1:
        item_prefix = item_prefix
    else:
        item_prefix = ""

    if title:
        pretty_list += f"{title}\n\n"

    if top:
        items = items[:top]

    for option in items:
        pretty_list += f"{item_prefix}{option}\n"

    return pretty_list


def write_code(
    content,
    schema,
    attribute_func,
    provider,
    scope,
    namespace='hashicorp',
    resource=None,
    block_hierarchy=[],
    documentation_url=None,
    block_func=None,
    resource_func=None,
    **kwargs,
):
    if resource_func:
        resource_header, resource_footer = resource_func(
            documentation_url=documentation_url, **kwargs
        )
        content += resource_header

    # Get the attributes and blocks from the schema
    attributes = schema.get("block", {}).get("attributes", {})
    blocks = schema.get("block", {}).get("block_types", {})

    # For each attribute
    for attribute, attribute_schema in attributes.items():
        # Call the function that formats code
        content = attribute_func(
            content=content,
            schema=attribute_schema,
            block_hierarchy=block_hierarchy,
            attribute=attribute,
            namespace=namespace,
            provider=provider,
            resource=resource,
            scope=scope,
            **kwargs,
        )

    # Recursively call this function on each block
    for block, block_schema in blocks.items():
        block_hierarchy.append(block)
        process_attributes = True

        # Set default headers and footers
        block_header, block_footer = None, None

        # Set block headers and footers if a block_func is passed
        if block_func:
            block_header, block_footer = block_func(
                block_schema, block, block_hierarchy, documentation_url, **kwargs
            )

        # Add a block header if one exists
        if block_header:
            content += (
                block_header  # Add header before processing the block's attributes
            )
        else:
            process_attributes = False

        if process_attributes:
            # Recurse through the child attributes
            content = write_code(
                content=content,
                schema=block_schema,
                attribute_func=attribute_func,
                block_hierarchy=block_hierarchy,
                namespace=namespace,
                provider=provider,
                resource=resource,
                scope=scope,
                block_func=block_func,
                **kwargs,
            )

        # Add a block footer if one exists:
        if block_footer:
            content += (
                block_footer  # Add footer after processing the block's attributes
            )

        del block_hierarchy[-1:]

    if resource_func:
        content += resource_footer

    return content


def wrap_text(text, line_length=80):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + word) + 1 <= line_length:
            if current_line:
                current_line += " "
            current_line += word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def add_resource_wrapper(header, documentation_url=None, comment=None, **kwargs):
    header_content = ""

    if documentation_url:
        header_content += f"# Terraform docs: {documentation_url}\n"

    if comment:
        max_line_length = 80
        wrapped_comment = "\n".join(["# " + line for line in wrap_text(text=comment)])
        header_content += f"{wrapped_comment}\n"

    header_content += f"{header}\n"
    footer = "}\n"

    return header_content, footer


def add_block_wrapper(
    schema,
    block,
    block_hierarchy,
    documentation_url=None,
    required_blocks_only=False,
    ignore_blocks=[],
    dynamic_blocks=[],
    **kwargs,
):
    header = ""

    # Set min and max items for block
    block_min_items = schema.get("min_items", None)
    block_max_items = schema.get("max_items", None)

    # Determine if the block is required
    required_block = is_required_block(block_min_items=block_min_items)

    # Skip blocks
    if (
        required_blocks_only
        and not required_block
        or "_".join(block_hierarchy) in ignore_blocks
        or required_block == None
    ):
        header = None
        footer = None
    else:
        # Write a comment describing the constraints of the block
        required_blocks_message = "required" if required_block else "optional"
        min_blocks_message = (
            "no minimum number of items"
            if block_min_items == None
            else f"a minimum of {block_min_items} items"
        )
        max_blocks_message = (
            "no maximum number of items"
            if block_max_items == None
            else f"a maximum of {block_max_items} items"
        )

        header += f"\n# This block is {required_blocks_message} with {min_blocks_message} and {max_blocks_message}\n"

        if "_".join(block_hierarchy) in dynamic_blocks:
            header += f'dynamic "{block}" {{\n  for_each = var.{"_".join(block_hierarchy)}\n  content {{\n'
            footer = "}\n}\n"
        else:
            header += f"{block} {{\n"
            footer = "}\n"

    return header, footer


def write_body_code(
    content,
    schema,
    provider,
    attribute,
    namespace="hashicorp",
    resource=None,
    scope=None,
    block_hierarchy=[],
    documentation_text=None,
    attribute_value_prefix="",
    attribute_defaults={},
    dynamic_blocks=[],
    required_attributes_only=False,
    ignore_attributes=[],
    add_descriptions=False,
    **kwargs,
):
    required_attribute = is_required_attribute(attribute_schema=schema)
    if (
        required_attributes_only
        and not required_attribute
        or "_".join(block_hierarchy + [attribute]) in ignore_attributes
        or required_attribute == None
    ):
        pass
    else:
        attribute = write_attribute(
            attribute=attribute,
            attribute_schema=schema,
            documentation_text=documentation_text,
            block_hierarchy=block_hierarchy,
            attribute_value_prefix=attribute_value_prefix,
            attribute_defaults=attribute_defaults,
            dynamic_blocks=dynamic_blocks,
            add_descriptions=add_descriptions
        )

        content += f"{attribute}\n"

    return content


def create_provider_code(
    provider,
    namespace="hashicorp",
    ignore_attributes=[],
    ignore_blocks=[],
    dynamic_blocks=[],
    required_attributes_only=False,
    required_blocks_only=False,
    add_descriptions=False,
    add_documentation_url=False,
    attribute_defaults={},
    attribute_value_prefix="",
    filename="providers.tf",
    comment=None,
    schema=None,
    refresh=False
):
    scope = "provider"
    header = f'provider "{provider}" {{'
    regex_pattern = rf'(?:#.*\n)*?^provider\s+"{provider}"\s+{{[\s\S]*?^}}$'

    if refresh:
        download_schema(filename=schema, refresh=refresh)

    schema = get_schema(
        namespace=namespace, provider=provider, scope=scope, filename=schema
    )

    if add_documentation_url:
        documentation_url = f"https://github.com/hashicorp/terraform-provider-{provider}"
    else:
        documentation_url = None

    code = write_code(
        schema=schema,
        attribute_func=write_body_code,
        namespace=namespace,
        provider=provider,
        scope=scope,
        content="",
        block_func=add_block_wrapper,
        resource_func=add_resource_wrapper,
        documentation_url=documentation_url,
        comment=comment,
        header=header,
        required_attributes_only=required_attributes_only,
        required_blocks_only=required_blocks_only,
        ignore_attributes=ignore_attributes,
        ignore_blocks=ignore_blocks,
        dynamic_blocks=dynamic_blocks,
        attribute_defaults=attribute_defaults,
        attribute_value_prefix=attribute_value_prefix,
        add_descriptions=add_descriptions
    )

    # Write file
    write_to_file(text=code, filename=filename, regex_pattern=regex_pattern)

    # Format code
    subprocess.run(["terraform", "fmt"], stdout=subprocess.DEVNULL)

    return code


def delete_provider_code(provider, filename="providers.tf"):
    regex_pattern = rf'^provider\s+"{provider}"\s+{{[\s\S]*?^}}\n*'

    with open(filename, "r") as f:
        string = f.read()

    result = re.sub(pattern=regex_pattern, repl="", string=string, flags=re.MULTILINE)

    with open(filename, "w") as f:
        f.write(result)


def create_resource_code(
    provider,
    resource,
    namespace="hashicorp",
    ignore_attributes=[],
    ignore_blocks=[],
    dynamic_blocks=[],
    required_attributes_only=False,
    required_blocks_only=False,
    add_descriptions=False,
    add_documentation_url=False,
    attribute_defaults={},
    attribute_value_prefix="",
    comment=None,
    filename="main.tf",
    name="main",
    schema=None,
    refresh=False
):
    scope = "resource"
    resource = "_".join([provider, resource]) if not provider in resource else resource
    header = f'resource "{resource}" "{name}" {{'
    regex_pattern = rf'(?:#.*\n)*?^resource\s+"{resource}"\s+"{name}"\s+{{[\s\S]*?^}}$'

    if refresh:
        download_schema(filename=schema, refresh=refresh)

    schema = get_schema(
        namespace=namespace,
        provider=provider,
        resource=resource,
        scope=scope,
        filename=schema,
    )

    if add_documentation_url or add_descriptions:
        documentation_url = get_resource_documentation_url(
            namespace=namespace, provider=provider, resource=resource, scope=scope
        )
    else:
        documentation_url = None

    if add_descriptions:
        documentation = get_resource_documentation(documentation_url=documentation_url)
    else:
        documentation = None

    code = write_code(
        schema=schema,
        attribute_func=write_body_code,
        namespace=namespace,
        provider=provider,
        resource=resource,
        scope=scope,
        documentation_text=documentation,
        content="",
        block_func=add_block_wrapper,
        resource_func=add_resource_wrapper,
        documentation_url=documentation_url,
        comment=comment,
        header=header,
        required_attributes_only=required_attributes_only,
        required_blocks_only=required_blocks_only,
        ignore_attributes=ignore_attributes,
        ignore_blocks=ignore_blocks,
        dynamic_blocks=dynamic_blocks,
        attribute_defaults=attribute_defaults,
        attribute_value_prefix=attribute_value_prefix,
        add_descriptions=add_descriptions
    )

    # Write file
    write_to_file(text=code, filename=filename, regex_pattern=regex_pattern)

    # Format code
    subprocess.run(["terraform", "fmt"], stdout=subprocess.DEVNULL)

    return code


def delete_resource_code(provider, resource, name, filename="main.tf"):
    resource = "_".join([provider, resource]) if not provider in resource else resource
    regex_pattern = (
        rf'(?:#.*\n)*?^resource\s+"{resource}"\s+"{name}"\s+{{[\s\S]*?^}}\n*'
    )

    with open(filename, "r") as f:
        string = f.read()

    result = re.sub(pattern=regex_pattern, repl="", string=string, flags=re.MULTILINE)

    with open(filename, "w") as f:
        f.write(result)


def create_data_source_code(
    provider,
    resource,
    namespace="hashicorp",
    ignore_attributes=[],
    ignore_blocks=[],
    dynamic_blocks=[],
    required_attributes_only=False,
    required_blocks_only=False,
    add_descriptions=False,
    add_documentation_url=False,
    attribute_defaults={},
    attribute_value_prefix="",
    comment=None,
    filename="data-sources.tf",
    name="main",
    schema=None,
    refresh=False
):
    scope = "data_source"
    resource = "_".join([provider, resource]) if not provider in resource else resource
    header = f'data "{resource}" "{name}" {{'
    regex_pattern = rf'(?:#.*\n)*?^data\s+"{resource}"\s+"{name}"\s+{{[\s\S]*?^}}$'

    if refresh:
        download_schema(filename=schema, refresh=refresh)

    schema = get_schema(
        namespace=namespace,
        provider=provider,
        resource=resource,
        scope=scope,
        filename=schema,
    )

    if add_documentation_url or add_descriptions:
        documentation_url = get_resource_documentation_url(
            namespace=namespace, provider=provider, resource=resource, scope=scope
        )
    else:
        documentation_url = None

    if add_descriptions:
        documentation = get_resource_documentation(documentation_url=documentation_url)
    else:
        documentation = None

    code = write_code(
        schema=schema,
        attribute_func=write_body_code,
        namespace=namespace,
        provider=provider,
        resource=resource,
        scope=scope,
        documentation_text=documentation,
        content="",
        block_func=add_block_wrapper,
        resource_func=add_resource_wrapper,
        documentation_url=documentation_url,
        comment=comment,
        header=header,
        required_attributes_only=required_attributes_only,
        required_blocks_only=required_blocks_only,
        ignore_attributes=ignore_attributes,
        ignore_blocks=ignore_blocks,
        dynamic_blocks=dynamic_blocks,
        attribute_defaults=attribute_defaults,
        attribute_value_prefix=attribute_value_prefix,
        add_descriptions=add_descriptions
    )

    # Write file
    write_to_file(text=code, filename=filename, regex_pattern=regex_pattern)

    # Format code
    subprocess.run(["terraform", "fmt"], stdout=subprocess.DEVNULL)

    return code


def delete_data_source_code(provider, resource, name, filename="main.tf"):
    resource = "_".join([provider, resource]) if not provider in resource else resource
    regex_pattern = rf'(?:#.*\n)*?^data\s+"{resource}"\s+"{name}"\s+{{[\s\S]*?^}}\n*'

    with open(filename, "r") as f:
        string = f.read()

    result = re.sub(pattern=regex_pattern, repl="", string=string, flags=re.MULTILINE)

    with open(filename, "w") as f:
        f.write(result)


# namespace = "hashicorp"
# provider = "azurerm"
# resource = "key_vault"
# scope = "data_source"

# create_data_source_code(provider=provider, resource=resource, name="main", attribute_value_prefix="test")
