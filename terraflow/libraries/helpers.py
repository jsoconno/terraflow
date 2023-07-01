import os
import re
import json
import requests
import subprocess
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from typing import List, Tuple, Optional
import difflib

from terraflow.libraries.constants import *

# File and folder manipulation functions.

def read_text_file(filename: str) -> str:
    """
    Read the contents of a text file.

    Args:
        filename: The name of the file to read.

    Returns:
        The contents of the text file as a string.
    """
    with open(filename, "r") as file:
        return file.read()

def write_text_file(filename: str, content: str) -> None:
    """
    Write content to a text file.

    Args:
        filename: The name of the file to write.
        content: The content to be written.
    """
    with open(filename, "w") as file:
        file.write(content)

def read_json_file(filename: str) -> dict:
    """
    Reads JSON from a file.

    Args:
        filename: The name of the file to read.

    Returns:
        A dictionary representing the JSON data.
    """
    with open(filename, "r") as json_file:
        return json.loads(json_file.read())

def write_json_file(filename: str, data: dict) -> None:
    """
    Writes data as JSON to a file.

    Args:
        filename: The name of the file to write.
        data: The data to be written as JSON.
    """
    with open(filename, "w") as f:
        json.dump(data, f)



# Formatting functions.

def format_list(items: list, title: str = None, top: int = None, prefix: str = " - ") -> str:
    """
    Format a list for output in the terminal.

    Args:
        items: The list of items to format.
        title: The optional title for the formatted list.
        top: The optional maximum number of items to include.
        prefix: The prefix string to prepend to each item.

    Returns:
        The formatted list as a string.
    """
    formatted_list = "\n"

    if title:
        formatted_list += f"{title}\n\n"

    if top:
        items = items[:top]

    for option in items:
        formatted_list += f"{prefix}{option}\n"

    return formatted_list

def colors(color: str = "END") -> str:
    """
    Returns ANSI color codes for printing to the command line.

    Args:
        color: The color name to retrieve the code for.

    Returns:
        The ANSI color code as a string.
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

def format_terminal_text():
    """
    Formats text for terminal output.
    """
    pass

# Helper functions

def calculate_levenshtein_distance(s: str, t: str) -> float:
    """
    Calculate the normalized Levenshtein distance between two strings.

    Args:
        s: The first string.
        t: The second string.

    Returns:
        The normalized Levenshtein distance between the two strings as a float.
    """
    # Convert the strings to lowercase
    s = s.lower()
    t = t.lower()

    # Initialize the distance matrix with zeros
    d = [[0 for _ in range(len(t) + 1)] for _ in range(len(s) + 1)]

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


def convert_strings_to_dict(text: str, delimiter: str = "=") -> dict:
    """
    Converts a string to a dictionary based on a delimiter.

    Args:
        text: The string to convert.
        delimiter: The delimiter used to split the string (default: "=").

    Returns:
        A dictionary created from the string, where the keys and values are separated by the delimiter.
    """
    dictionary = {}
    for x in text:
        k, v = x.split(delimiter)
        dictionary[k] = v

    return dictionary

def scrape_website(url: str, tag: str = None, selector: str = None, list_output: bool = False) -> str:
    """
    Scrape content from a URL. If a tag or selector is specified, only content within that tag or selector is scraped.

    Args:
        url: The URL to scrape.
        tag: Optional; an HTML tag name to scrape (e.g. "p" for paragraph tags, "div" for div tags, etc.).
        selector: Optional; a CSS selector to scrape.
        list_output: Optional; whether to return the output as a list (default is False).

    Returns:
        The scraped content as a string or a list of strings.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        response.raise_for_status()  # If the response contains an HTTP error status code, raise an exception
    except RequestException as e:
        print(f"Failed to get the webpage. Error: {e}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    if tag:
        elements = soup.find_all(tag)
    elif selector:
        elements = soup.select(selector)
    else:
        return '\n'.join(line.strip() for line in soup.text.split('\n') if line.strip())

    texts = ['\n'.join(line.strip() for line in elem.get_text().split('\n') if line.strip()) for elem in elements]

    if list_output:
        return texts
    else:
        return '\n'.join(texts)

def format_attribute_type(attribute_type):
    """
    Formats the attribute type from the provider schema for use in variables.
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

# File and folder manipulation functions.

def read_text_file(filename: str) -> str:
    """
    Read the contents of a text file.

    Args:
        filename: The name of the file to read.

    Returns:
        The contents of the text file as a string.
    """
    with open(filename, "r") as file:
        return file.read()

def write_text_file(filename: str, content: str) -> None:
    """
    Write content to a text file.

    Args:
        filename: The name of the file to write.
        content: The content to be written.
    """
    with open(filename, "w") as file:
        file.write(content)

def read_json_file(filename: str) -> dict:
    """
    Reads JSON from a file.

    Args:
        filename: The name of the file to read.

    Returns:
        A dictionary representing the JSON data.
    """
    with open(filename, "r") as json_file:
        return json.loads(json_file.read())

def write_json_file(filename: str, data: dict) -> None:
    """
    Writes data as JSON to a file.

    Args:
        filename: The name of the file to write.
        data: The data to be written as JSON.
    """
    with open(filename, "w") as f:
        json.dump(data, f)

def read_files(file_extensions: list = ['.tf']) -> str:
    """
    Loop through all files with the provided extensions in the current directory and return a single string with all code.

    Args:
        file_extensions (List[str], optional): List of file extensions to include. Defaults to ['.tf'].

    Returns:
        str: A string containing the contents of the files.
    """
    content = ""
    for file_name in os.listdir(os.getcwd()):
        if any(file_name.endswith(extension) for extension in file_extensions):
            with open(file_name, 'r') as file:
                content += file.read() + '\n'

    return content

def write_terraform_to_file(filename: str, new_code: str):#, provider=None, resource=None):
    """
    Write a Terraform provider, resource, data source, variable, or output block to a file based on a regex pattern.

    Args:
        filename (str): The name of the file where the Terraform block will be written.
        new_code (str): The new Terraform code to be written to the file.
    """
    # Try to read the existing contents of the file
    try:
        with open(filename, "r+") as f:
            contents = f.read()
    except FileNotFoundError:
        contents = ""

    # If the file isn't empty and doesn't end with a newline, append a newline
    if contents and not contents.endswith("\n"):
        contents += "\n\n"

    # Define regex pattern that can be used to collect all objects, regardless of type
    pattern = r'(((?:#.*\n)*?^(.*?)\s+(?:"(.*?)"\s+)?\s?"(.*?)"\s+{)[\s\S]*?^}$)'

    # Split new_code into blocks
    old_code_blocks = re.findall(pattern, contents, flags=re.MULTILINE)
    new_code_blocks = re.findall(pattern, new_code, flags=re.MULTILINE)

    # Construct dictionaries for old and new blocks using block type and name as keys
    old_blocks_dict = {block_id: code for code, block_id, block_type, resource_type, name in old_code_blocks}
    new_blocks_dict = {block_id: code for code, block_id, block_type, resource_type, name in new_code_blocks}

    # Merge old and new blocks dictionaries
    merged_blocks_dict = {**old_blocks_dict, **new_blocks_dict}

    # Construct the final contents by joining all the blocks in merged_blocks_dict
    merged_code = "\n\n".join(block for block in merged_blocks_dict.values())

    # Write the new contents back to the file
    with open(filename, "w+") as f:
        f.write(merged_code.strip())

    return merged_code

def remove_unused_variables():
    """
    This function collects all code, collects all variables, determines which ones to delete, and deletes them.
    """
    code = read_files()

    # Collect all variables from the configuration
    pattern = r'.*?\s+=\s+var.(.*?)(?:\s|#)'
    variables_list = re.findall(pattern, code, re.MULTILINE)

    # Establish a pattern for collecting all variable declarations
    pattern = r'((?:#.*\n)*?^variable\s+(?:".*?"\s+)?\s?"(.*?)"\s+{[\s\S]*?^}$)'
    variable_declarations = re.findall(pattern, code, re.MULTILINE)
    variable_declarations_dict = {variable: code for code, variable in variable_declarations}

    # Create a list of items that are in variable_declarations_dict that are not in variables_list
    unused_variables = [var for var in variable_declarations_dict.keys() if var not in variables_list]

    # Loop through each item in the unused_variables list and do a find an replace to remove code
    for var in unused_variables:
        # replace the unused variables in the code string
        code = code.replace(variable_declarations_dict[var], "")

    # Now we'll write the modified code back into the Terraform files
    for file_name in os.listdir(os.getcwd()):
        if any(file_name.endswith(extension) for extension in ".tf"):
            with open(file_name, 'r') as file:
                file_content = file.read()
            for var in unused_variables:
                # replace the unused variables in each file's content
                file_content = file_content.replace(variable_declarations_dict[var], "")
            # Now write the modified content back into the file
            with open(file_name, 'w') as file:
                file.write(file_content)

remove_unused_variables()

# Formatting functions.

def format_list(items: list, title: str = None, top: int = None, prefix: str = " - ") -> str:
    """
    Format a list for output in the terminal.

    Args:
        items: The list of items to format.
        title: The optional title for the formatted list.
        top: The optional maximum number of items to include.
        prefix: The prefix string to prepend to each item.

    Returns:
        The formatted list as a string.
    """
    formatted_list = "\n"

    if title:
        formatted_list += f"{title}\n\n"

    if top:
        items = items[:top]

    for option in items:
        formatted_list += f"{prefix}{option}\n"

    return formatted_list

def colors(color: str = "END") -> str:
    """
    Returns ANSI color codes for printing to the command line.

    Args:
        color: The color name to retrieve the code for.

    Returns:
        The ANSI color code as a string.
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

def format_terminal_text():
    """
    Formats text for terminal output.
    """
    pass

def format_terraform_code(code: str, indentation='  '):
    """
    Indent Terraform code so that it is formatted correctly.

    Args:
        code (str): The Terraform code to format.
        indentation (str): The string used for each level of indentation. Defaults to two spaces.
    """

    # Split the code into lines
    lines = code.split('\n')

    # Initialize a counter for the current level of indentation
    indent_level = 0

    # Process each line
    for i, line in enumerate(lines):
        # Increase the indent level if the line opens a block
        if '{' in line and '}' not in line:
            lines[i] = indent_level * indentation + line.lstrip()
            indent_level += 1
        # Decrease the indent level if the line closes a block
        elif '}' in line and '{' not in line:
            indent_level -= 1
            lines[i] = indent_level * indentation + line.lstrip()
        # No change in indent level if the line both opens and closes a block
        elif '{' in line and '}' in line:
            lines[i] = indent_level * indentation + line.lstrip()
        # Otherwise, just add the current level of indentation
        else:
            lines[i] = indent_level * indentation + line.lstrip()

    # Join the lines back together and return the result
    return '\n'.join(lines)

# Helper functions

def calculate_levenshtein_distance(s: str, t: str) -> float:
    """
    Calculate the normalized Levenshtein distance between two strings.

    Args:
        s: The first string.
        t: The second string.

    Returns:
        The normalized Levenshtein distance between the two strings as a float.
    """
    # Convert the strings to lowercase
    s = s.lower()
    t = t.lower()

    # Initialize the distance matrix with zeros
    d = [[0 for _ in range(len(t) + 1)] for _ in range(len(s) + 1)]

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


def convert_strings_to_dict(text: str, delimiter: str = "=") -> dict:
    """
    Converts a string to a dictionary based on a delimiter.

    Args:
        text: The string to convert.
        delimiter: The delimiter used to split the string (default: "=").

    Returns:
        A dictionary created from the string, where the keys and values are separated by the delimiter.
    """
    dictionary = {}
    for x in text:
        k, v = x.split(delimiter)
        dictionary[k] = v

    return dictionary


def is_valid_version(version: str, valid_versions: list) -> bool:
    """
    Checks whether a provided version is valid based on a given list.

    Args:
        version: The version to validate.
        valid_versions: A list of valid versions.

    Returns:
        True if the version is valid, False otherwise.
    """
    return version in valid_versions

def scrape_website(url: str, tag: str = None, selector: str = None, list_output: bool = False) -> str:
    """
    Scrape content from a URL. If a tag or selector is specified, only content within that tag or selector is scraped.

    Args:
        url: The URL to scrape.
        tag: Optional; an HTML tag name to scrape (e.g. "p" for paragraph tags, "div" for div tags, etc.).
        selector: Optional; a CSS selector to scrape.
        list_output: Optional; whether to return the output as a list (default is False).

    Returns:
        The scraped content as a string or a list of strings.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        response.raise_for_status()  # If the response contains an HTTP error status code, raise an exception
    except RequestException as e:
        print(f"Failed to get the webpage. Error: {e}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    if tag:
        elements = soup.find_all(tag)
    elif selector:
        elements = soup.select(selector)
    else:
        return '\n'.join(line.strip() for line in soup.text.split('\n') if line.strip())

    texts = ['\n'.join(line.strip() for line in elem.get_text().split('\n') if line.strip()) for elem in elements]

    if list_output:
        return texts
    else:
        return '\n'.join(texts)

# Documentation functions.

def get_terraform_documentation_url(namespace: str, provider: str, resource: str, scope: str, version: str = 'main') -> str:
    """
    Get the documentation URL for a provider resource or data source.

    Args:
        namespace: The namespace of the provider.
        provider: The provider name.
        resource: The resource or data source name.
        scope: The scope of the documentation (resource or data source).
        version: The version of the provider (default: 'main').

    Returns:
        The documentation URL as a string.
    """
    url = f"https://registry.terraform.io/v1/providers/{namespace}/{provider}"
    response = json.loads(requests.get(url).text)

    docs_path = None

    for doc in response["docs"]:
        if (
            doc["title"] == resource
            or doc["title"] == resource.replace(f"{provider}_", "")
        ) and doc["category"] == f"{scope.replace('_', '-')}s":
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

def get_terraform_documentation(namespace: str, provider: str, scope: str, resource: str, version: str = 'main', cache: bool = True) -> str:
    """
    Get the documentation for a provider resource or data source and cache it.

    Args:
        namespace: The namespace of the provider.
        provider: The provider name.
        scope: The scope of the documentation (resource or data source).
        resource: The resource or data source name.
        version: The version of the provider (default: 'main').
        cache: Whether to cache the documentation (default: True).

    Returns:
        The documentation content as a string.
    """
    # Determine the filename for the cached documentation
    filename = f"{namespace}.{provider}.{resource}.{scope}.txt"
    path = os.path.join(DOCUMENTATION_DIR, filename)

    # If the file exists, read the cached documentation
    if os.path.exists(path):
        print(f'\n{colors("OK_BLUE")}Info:{colors()} Reading documentation from cache for the {namespace} {provider} {resource} {scope}.\n')
        return read_text_file(path)

    # If the file does not exist, get the documentation URL and the documentation
    documentation_url = get_terraform_documentation_url(namespace, provider, resource, scope, version)
    documentation = scrape_website(documentation_url, tag="article")

    # If caching is enabled, cache the documentation
    if cache:
        try:
            if not os.path.exists(DOCUMENTATION_DIR):
                os.makedirs(DOCUMENTATION_DIR)

            write_text_file(path, documentation)

            print(f'\n{colors("OK_GREEN")}Success:{colors()} Documentation read and cached successfully for the {namespace} {provider} {resource} {scope}.\n')
        except Exception:
            print(f'\n{colors("FAIL")}Error:{colors()} An error occurred while caching the documentation.\n')

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
                normalized_distance = calculate_levenshtein_distance(match, normalized_block_text)
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

# namespace = "hashicorp"
# provider = "azurerm"
# resource = "key_vault"
# scope = "resource"

# get_terraform_documentation(namespace, provider, scope, resource, cache=True)

# Version functions.

def get_semantic_version(version: str) -> Optional[Tuple[int, int, int, int]]:
    """
    Get a tuple representing the semantic version components including major, minor, patch, and pre-release.

    Args:
        version (str): The version string.

    Returns:
        Optional[Tuple[int, int, int, int]]: A tuple containing the version components or None if the version is invalid.
    """
    regex_pattern = r'(\d+)\.*(\d+)*\.*(\d+)*(?:-*(?:(?:[a-zA-Z]*(\d*)))?)'

    try:
        match = re.match(regex_pattern, version)
        if match:
            version_components = match.groups()
            version_components = tuple(int(component) if component is not None else 0 for component in version_components)
            version_length = len(version_components)
            missing_version_components = 4 - version_length

            if missing_version_components > 0:
                # Adding the version length at the end is used for pessimistic constraint operator logic.
                version_components += (0,) * (missing_version_components - 1) + (1000000000000000,) + (version_length,)

            return version_components
    except Exception:
        pass

    return None

def sort_versions(versions: List[str], reverse: bool = True) -> List[str]:
    """
    Sorts lists of versions based on the semantic version.

    Args:
        versions (List[str]): The list of versions to sort.
        reverse (bool, optional): Determines whether to sort in ascending (False) or descending (True) order.
                                  Defaults to True.

    Returns:
        List[str]: The sorted list of versions.
    """
    tuple_versions = [get_semantic_version(version) for version in versions]
    versions = [x for _, x in sorted(zip(tuple_versions, versions), reverse=reverse)]
    return versions

def is_valid_version(version: str, valid_versions: list) -> bool:
    """
    Checks whether a provided version is valid based on a given list.

    Args:
        version: The version to validate.
        valid_versions: A list of valid versions.

    Returns:
        True if the version is valid, False otherwise.
    """
    return version in valid_versions

# versions = ["1.0.0", "1.1.0", "0.1.3", "0.1.1-alpha", "2.0.0"]
# print(sort_versions(versions))

def handle_attribute(attribute, attribute_schema, block_hierarchy, config, documentation_text):
    # Skip items that are in the exclude_attributes list or that are computed and not required
    if not attribute_schema.get('required', False) and (
            attribute_schema.get('computed', False) or "_".join(block_hierarchy + [attribute]) in config.get(
            'exclude_attributes', [])):
        return None, None, None, None

    # Get attribute description from the pre-loaded documentation
    description = ""
    if documentation_text and config.get('add_descriptions', False):
        description = get_resource_attribute_description(documentation_text, attribute, block_hierarchy)

    # Construct the attribute name
    if block_hierarchy:
        attribute_name = "_".join(block_hierarchy + [attribute])
    else:
        attribute_name = attribute

    # Check if the attribute is optional
    optional = attribute_schema.get('optional', False)
    
    # Get and format attribute type
    attribute_type = attribute_schema.get('type')
    formatted_type = format_attribute_type(attribute_type)

    return attribute_name, description, optional, formatted_type

def list_items(schema, namespace="hashicorp", provider=None, scope="resource", keywords=None):
    """
    Get a list of providers for a namespace or resources or data sources for a provider.
    
    Parameters:
    schema (dict): The schema dictionary containing provider information.
    namespace (str): The namespace of the provider, defaults to 'hashicorp'.
    provider (str): The specific provider to consider, defaults to None.
    scope (str): The scope to consider (either 'provider' or 'resource'), defaults to 'resource'.
    keywords (list): A list of keywords to filter the items, defaults to None.

    Returns:
    list: A list of items based on the provided configuration.
    """
    items = []

    try:
        if scope == "provider":
            schema = schema["provider_schemas"]
            for provider_name in schema:
                provider_name = provider_name.replace("registry.terraform.io/", "").split("/")[1]
                items.append(provider_name)
        elif scope in ALLOWED_SCOPES:
            schema = schema["provider_schemas"][
                f"registry.terraform.io/{namespace}/{provider}"
            ][f"{scope}_schemas"]
            for source in schema:
                items.append(source.replace(f"{provider}_", ""))
        else:
            print(f"The scope must be one of {ALLOWED_SCOPES}.")
    except KeyError:
        print("No items were found.")

    if keywords:
        items = [item for item in items if any(keyword in item for keyword in keywords)]

    return items

def delete_provider_code(provider, filename="providers.tf"):
    regex_pattern = rf'^provider\s+"{provider}"\s+{{[\s\S]*?^}}\n*'

    with open(filename, "r") as f:
        string = f.read()

    result = re.sub(pattern=regex_pattern, repl="", string=string, flags=re.MULTILINE)

    with open(filename, "w") as f:
        f.write(result)

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

def delete_data_source_code(provider, resource, name, filename="main.tf"):
    resource = "_".join([provider, resource]) if not provider in resource else resource
    regex_pattern = rf'(?:#.*\n)*?^data\s+"{resource}"\s+"{name}"\s+{{[\s\S]*?^}}\n*'

    with open(filename, "r") as f:
        string = f.read()

    result = re.sub(pattern=regex_pattern, repl="", string=string, flags=re.MULTILINE)

    with open(filename, "w") as f:
        f.write(result)

def run_terraform_fmt():
    subprocess.run(["terraform", "fmt"], stdout=subprocess.DEVNULL)