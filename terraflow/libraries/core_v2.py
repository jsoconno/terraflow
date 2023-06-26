import json
# from pathlib import Path
import subprocess
import traceback
import requests
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
        print(f'\n{colors("OK_BLUE")}Tip:{colors()} A schema is already downloaded. To refresh the schema, rerun this command with the `--refresh` flag.\n')
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

def get_documentation_url(namespace: str, provider: str, resource: str, scope: str, version: str = 'main') -> str:
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

def get_documentation(documentation_url: str) -> str:
    """
    Get the documentation content from a URL.

    Args:
        documentation_url: The URL of the documentation.

    Returns:
        The documentation content as a string.
    """
    # TODO: add logic to only capture the actual content, not the header and footer info, for example.
    if documentation_url:
        html_text = requests.get(documentation_url).content.decode()
        soup = BeautifulSoup(html_text, features="html.parser")

        # Extract the text from the HTML document while preserving special characters
        documentation = re.sub(r"<[^>]*>", "", soup.text)  # Remove all HTML tags
        documentation = re.sub(r"(\n\s*)+", "\n", documentation)  # Normalize newlines
        documentation = documentation.strip()
    else:
        print(f'\n{colors(color="WARNING")}Warning:{colors()} The documentation URL is not available.\n')
        documentation = None

    return documentation

def cache_documentation(namespace: str, provider: str, scope: str, resource: str, documentation: str) -> None:
    """
    Store documentation for a provider resource or data source locally.

    Args:
        namespace: The namespace of the provider.
        provider: The provider name.
        scope: The scope of the documentation (resource or data source).
        resource: The resource or data source name.
        documentation: The documentation content to be cached.
    """
    # TODO: Remember to add the provider version later once we have a function to get it.
    filename = f"{namespace}.{provider}.{scope}.{resource}.txt"
    path = os.path.join(DOCUMENTATION_DIR, filename)

    try:
        if not os.path.exists(DOCUMENTATION_DIR):
            os.makedirs(DOCUMENTATION_DIR)

        write_text_file(path, documentation)

        print(f'\n{colors("OK_GREEN")}Success:{colors()} Documentation cached successfully.\n')
    except Exception:
        print(f'\n{colors("FAIL")}Error:{colors()} An error occurred while caching the documentation.\n')

namespace = "hashicorp"
provider = "azurerm"
resource = "key_vault"
scope = "resource"

documentation_url = get_documentation_url(namespace, provider, resource, scope)
documentation = get_documentation(documentation_url)
print(documentation)

cache_documentation(namespace, provider, scope, resource, documentation)

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

def list_terraform_versions():
    """
    Get a list of valid Terraform versions.
    """
    pass

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

def get_provider_versions():
    """
    Get a list of all valid Terraform provider versions.
    """
    pass

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

# Helper functions

def calculate_levenshtein_distance():
    """
    Calculate the normalized levenshtein distance between two strings.
    """
    pass

def convert_strings_to_dict():
    """
    Converts a string to a dictionary based on a delimiter.
    """
    pass

def validate_version():
    """
    Checks whether or not a provided Terraform or provider version is valid.
    """
    pass