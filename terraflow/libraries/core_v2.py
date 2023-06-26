import json
# from pathlib import Path
import subprocess
import traceback
# import requests
# from bs4 import BeautifulSoup
# import re
# import os
# import difflib
# import errno

from terraflow.libraries.constants import *

# For this new setup, there should be a `.terraflow` folder added
# to each project.  Inside that folder should be a schemas folder
# and a docs folder where those artifacts can be cached.

# File and folder manipulation functions.

def write_terraform_to_file():
    """
    Write a Terraform provider, resource, data source, variable, or output block to a file based on a regex pattern.
    """
    pass

def read_json_file(filename):
    """
    Reads json from a file.
    """
    with open(filename, "r") as json_file:
        return json.loads(json_file.read())

def write_json_file(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)

# Formatting functions.

def format_list(items: list, title: str = None, top: int = None, prefix: str = " - "):
    """
    Format a list for output in the terminal.
    """
    formatted_list = "\n"

    if title:
        formatted_list += f"{title}\n\n"

    if top:
        items = items[:top]

    for option in items:
        formatted_list += f"{prefix}{option}\n"

    return formatted_list

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

# Schema functions.

def get_schema(filename=None):
    """
    Returns the schema for a provider as a dictionary.
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

def fetch_schema():
    """
    Gets a provider schema from Terraform.
    """
    try:
        p = subprocess.run(["terraform", "init"], capture_output=True, text=True)
        return json.loads(subprocess.check_output(["terraform", "providers", "schema", "-json"]).decode("utf-8"))
    except subprocess.CalledProcessError:
        print(
            f'\n{colors(color="WARNING")}Warning:{colors()} The provider versions for this configuration have changed.  Running an upgrade.\n'
        )
        p = subprocess.run(["terraform", "init", "-upgrade"], capture_output=True, text=True)
        return json.loads(subprocess.check_output(["terraform", "providers", "schema", "-json"]).decode("utf-8"))

def cache_schema(schema=None, filename=".terraflow/schema.json", refresh=False):
    """
    Cache the downloaded Terraform schema as ".terraflow/schema.json".
    """
    _, ext = os.path.splitext(filename)
    if ext.lower() != ".json":
        print(f'\n{colors("FAIL")}Error:{colors()} {filename} is not a json file.\n')
        return

    if os.path.exists(filename) and not refresh:
        print(f'\n{colors("OK_BLUE")}Tip:{colors()} A schema is already downloaded.  To refresh the schema, rerun this command with the `--refresh` flag.\n')
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

def get_provider_schema(schema, namespace, provider):
    """
    Get the schema for a given provider.
    """
    return schema["provider_schemas"][f"{TERRAFORM_REGISTRY_BASE}/{namespace}/{provider}"]["provider"]

def get_resource_schema(schema, namespace, provider, resource):
    """
    Get the schema for a given provider resource.
    """
    # Allow resource shorthand without the provider
    if resource and not provider in resource:
        resource = f"{provider}_{resource}"

    return schema["provider_schemas"][f"{TERRAFORM_REGISTRY_BASE}/{namespace}/{provider}"]["resource_schemas"][resource]

def get_data_source_schema(schema, namespace, provider, data_source):
    """
    Get the schema for a given provider data source.
    """
    # Allow resource shorthand without the provider
    if data_source and not provider in data_source:
        data_source = f"{provider}_{data_source}"

    return schema["provider_schemas"][f"{TERRAFORM_REGISTRY_BASE}/{namespace}/{provider}"]["data_source_schemas"][resource]

def get_attribute_schema(schema, blocks=None, attribute=None):
    """
    Get the schema for a given provider, resource, or data source attribute.
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

def get_documentation_url():
    """
    Get the url where the documentation exists.
    """
    pass

def get_documentation():
    """
    Get documentation for a provider resource or data source from the internet.
    """
    pass

def cache_documentation():
    """
    Store documentation for a provider resource or data source locally.
    """
    pass

def format_terminal_text():
    """
    Formats text for terminal output.
    """
    pass

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