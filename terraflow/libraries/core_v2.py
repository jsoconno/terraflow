import json
# from pathlib import Path
import subprocess
import traceback
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re
import os
# import difflib
# import errno

from terraflow.libraries.constants import *

# For this new setup, there should be a `.terraflow` folder added
# to each project.  Inside that folder should be a schemas folder
# and a docs folder where those artifacts can be cached.

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

def write_terraform_to_file():
    """
    Write a Terraform provider, resource, data source, variable, or output block to a file based on a regex pattern.
    """
    pass

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

# Schema functions.

def get_schema(filename: str = None) -> dict:
    """
    Returns the schema for a provider as a dictionary.

    Args:
        filename: The optional filename of the schema JSON file.

    Returns:
        The schema dictionary.
    """
    # Create the .terraflow directory if it doesn't already exist
    if not os.path.exists(TERRAFLOW_DIR):
        os.makedirs(TERRAFLOW_DIR)

    # Get the schema from file
    if filename and os.path.exists(filename):
        schema = read_json_file(filename)
    else:
        schema = fetch_schema()

    return schema

def fetch_schema() -> dict:
    """
    Gets a provider schema from Terraform.

    Returns:
        The schema dictionary fetched from Terraform.
    """
    try:
        p = subprocess.run(["terraform", "init"], capture_output=True, text=True)
        return json.loads(subprocess.check_output(["terraform", "providers", "schema", "-json"]).decode("utf-8"))
    except subprocess.CalledProcessError:
        print(
            f'\n{colors(color="WARNING")}Warning:{colors()} The provider versions for this configuration have changed. Running an upgrade.\n'
        )
        p = subprocess.run(["terraform", "init", "-upgrade"], capture_output=True, text=True)
        return json.loads(subprocess.check_output(["terraform", "providers", "schema", "-json"]).decode("utf-8"))

def cache_schema(schema: dict = None, filename: str = ".terraflow/schema.json", refresh: bool = False) -> None:
    """
    Cache the downloaded Terraform schema as ".terraflow/schema.json".

    Args:
        schema: The schema dictionary to be cached.
        filename: The filename to save the schema as.
        refresh: Flag indicating whether to refresh the schema if it already exists.
    """
    _, ext = os.path.splitext(filename)
    if ext.lower() != ".json":
        print(f'\n{colors("FAIL")}Error:{colors()} {filename} is not a JSON file.\n')
        return

    if os.path.exists(filename) and not refresh:
        print(f'\n{colors("OK_BLUE")}Info:{colors()} A schema is already downloaded. To refresh the schema, rerun this command with the `--refresh` flag.\n')
    else:
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        try:
            if schema is None:
                schema = get_schema()
            write_json_file(filename, schema)
            print(f'\n{colors("OK_GREEN")}Success:{colors()} Schema downloaded successfully.\n')
        except Exception as e:
            print(f'\n{colors("FAIL")}Error:{colors()} An error occurred while caching the schema: {traceback.format_exc()}\n')

def get_provider_schema(schema: dict, namespace: str, provider: str) -> dict:
    """
    Get the schema for a given provider.

    Args:
        schema: The schema dictionary.
        namespace: The provider's namespace.
        provider: The provider name.

    Returns:
        The schema for the given provider.
    """
    return schema["provider_schemas"][f"{TERRAFORM_REGISTRY_BASE}/{namespace}/{provider}"]["provider"]

def get_resource_schema(schema: dict, namespace: str, provider: str, resource: str) -> dict:
    """
    Get the schema for a given provider resource.

    Args:
        schema: The schema dictionary.
        namespace: The provider's namespace.
        provider: The provider name.
        resource: The resource name.

    Returns:
        The schema for the given provider resource.
    """
    # Allow resource shorthand without the provider
    if resource and provider not in resource:
        resource = f"{provider}_{resource}"

    return schema["provider_schemas"][f"{TERRAFORM_REGISTRY_BASE}/{namespace}/{provider}"]["resource_schemas"][resource]

def get_data_source_schema(schema: dict, namespace: str, provider: str, data_source: str) -> dict:
    """
    Get the schema for a given provider data source.

    Args:
        schema: The schema dictionary.
        namespace: The provider's namespace.
        provider: The provider name.
        data_source: The data source name.

    Returns:
        The schema for the given provider data source.
    """
    # Allow data source shorthand without the provider
    if data_source and provider not in data_source:
        data_source = f"{provider}_{data_source}"

    return schema["provider_schemas"][f"{TERRAFORM_REGISTRY_BASE}/{namespace}/{provider}"]["data_source_schemas"][data_source]

def get_attribute_schema(schema: dict, blocks: list = None, attribute: str = None) -> dict:
    """
    Get the schema for a given provider, resource, or data source attribute.

    Args:
        schema: The schema dictionary.
        blocks: The list of blocks to traverse.
        attribute: The attribute name.

    Returns:
        The schema for the given attribute.
    """
    try:
        if blocks:
            # Loop over all blocks in the blocks list
            for block in blocks:
                # Go down into blocks until desired block is found
                schema = schema["block"]["block_types"].get(block, None)

        return schema["block"]["attributes"].get(attribute, None)
    except Exception:
        print(f'Error while trying to get the attribute schema: {traceback.format_exc()}')

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
    Get the documentation for a provider resource or data source and cache it if required.

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
        print(f'\n{colors("OK_BLUE")}Info:{colors()} Reading documentation from cache.\n')
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

            print(f'\n{colors("OK_GREEN")}Success:{colors()} Documentation read and cached successfully.\n')
        except Exception:
            print(f'\n{colors("FAIL")}Error:{colors()} An error occurred while caching the documentation.\n')

    return documentation


namespace = "hashicorp"
provider = "azurerm"
resource = "key_vault"
scope = "resource"

get_terraform_documentation(namespace, provider, scope, resource, cache=True)

# Shared functions.

def get_object_list():
    """
    Get a list of providers for a namespace or resources or data sources for a provider.
    """
    pass

def set_object_attribute_value():
    """
    Explicitly set the value for a provider, resource, or data source attribute.
    """
    pass

def recurse_schema():
    """
    Recurse the schema to write providers, resources, data sources, outputs, and variables.
    """
    pass

# Consider writing a reusable function for returning available
# providers, resources, and data sources and using that for each
# of the individual list functions.

# Terraform functions.

def create_terraform():
    """
    Create a terraform block.
    """
    pass

def delete_terraform():
    """
    Delete a terraform block.
    """
    pass

def get_terraform_versions() -> list:
    """
    Gets a list of Terraform versions.

    Returns:
        A list of valid Terraform versions.
    """
    response = requests.get("https://releases.hashicorp.com/terraform")
    
    pattern = r'terraform_((\d+)\.*(\d+)*\.*(\d+)*-?([\S]*))</a>'
    versions = re.findall(pattern, response.text)

    versions = [version[0] for version in versions]

    return versions

# print(get_terraform_versions())

def get_terraform_version():
    """
    Get the current Terraform version from the terraform block..
    """
    pass

def set_terraform_version():
    """
    Set the Terraform version in the terraform block.
    """
    pass

# Backend functions.

def create_backend():
    """
    Create a backend block.
    """
    pass

def delete_backend():
    """
    Delete a backend block.
    """
    pass

def get_backend():
    """
    Get the current backend.
    """
    pass

def set_backend():
    """
    Set the backend.
    """
    pass

# Provider functions.

def create_providers():
    """
    Create a Terraform provider block(s).
    """
    pass

def delete_providers():
    """
    Delete a Terraform provider block(s).
    """
    pass

def list_providers():
    """
    List the providers in the configuration.
    """
    pass

def get_providers():
    """
    Get a list of all available providers for a given namespace.
    """
    pass

def get_provider_version():
    """
    Get the current version of a given provider in the configuration.
    """
    pass

def get_provider_versions(namespace: str, provider: str) -> list:
    """
    Gets a list of versions for a given Terraform provider.

    Args:
        namespace: The namespace of the provider.
        provider: The provider name.

    Returns:
        A list versions for the provider.
    """
    url = f"https://registry.terraform.io/v1/providers/{namespace}/{provider}"
    response = requests.get(url)
    data = json.loads(response.text)

    versions = data["versions"]

    return versions

# print(get_provider_versions("hashicorp", "azurerm"))

def set_provider_version():
    """
    Set a provider version in the Terraform block.
    """
    pass

def set_provider_header():
    """
    Set the header content for a provider (e.g. comments, docs links, etc.).
    """
    pass

# Resource functions.

def create_resources():
    """
    Create a Terraform resource block(s).
    """
    pass

def delete_resources():
    """
    Delete a Terraform resource block(s).
    """
    pass

def list_resources():
    """
    List the resources in the configuration.
    """
    pass

def get_resources():
    """
    Get a list of all available resources for a given provider.
    """
    pass

def set_resource_header():
    """
    Set the header content for a resource (e.g. comments, docs links, etc.).
    """
    pass

# Data source functions.

def create_data_sources():
    """
    Create a Terraform data source block(s).
    """
    pass

def delete_data_sources():
    """
    Delete a Terraform data source block(s).
    """
    pass

def list_data_sources():
    """
    List the data sources in the configuration.
    """
    pass

def get_data_sources():
    """
    Get a list of all available data sources for a given provider.
    """
    pass

def set_data_source_header():
    """
    Set the header content for a resource (e.g. comments, docs links, etc.).
    """
    pass

# Variable functions.

def create_variables():
    """
    Create a Terraform variable block(s).
    """
    pass

def delete_variables():
    """
    Delete a Terraform variable block(s).
    """
    pass

def list_variables():
    """
    List the variables in the configuration.
    """
    pass

def get_variables():
    """
    Get a list of all available variables for a given provider.
    """
    pass

def delete_unused_variables():
    """
    Delete variables that are declared, but not used in the configuration.
    """
    pass

def set_variable_validation():
    """
    Add validation to a variable.  Supports equal, not equal, contains, not contains, and regex.
    """
    pass

def set_variable_attribute():
    """
    Explicitly sets a variables type, description, or default value.
    """
    pass

# Output functions.

def create_outputs():
    """
    Create a Terraform output block(s).
    """
    pass

def delete_outputs():
    """
    Delete a Terraform output block(s).
    """
    pass

def list_outputs():
    """
    List the outputs in the configuration.
    """
    pass

def get_outputs():
    """
    Get a list of all available outputs for a given provider.
    """
    pass

def set_output_attribute():
    """
    Explicitly sets an outputs value, description, or sensitive flag.
    """
    pass

# Provider, resource, and data source attribute functions.

def get_attributes():
    """
    Get a list of attributes for a given provider, resource, or data source.
    """
    pass

def get_attribute_description():
    """
    Get the description for a provider, resource, or data source attribute.
    """
    pass

def set_attribute_value():
    """
    Sets the value for a given resource or data source attribute.
    """
    pass

def format_attribute_type():
    """
    Formats the attribute type from the provider schema for use in variables.
    """
    pass

def is_required_attribute():
    """
    Determines if an attribute is required based on the schema.
    """
    pass

# Block functions.

def set_block_header():
    """
    Set the header content for a block (e.g. comments, docs links, etc.).
    """
    pass

def is_required_block():
    """
    Determines if a block is required based on the schema.
    """
    pass
