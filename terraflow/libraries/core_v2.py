import json
# from pathlib import Path
import subprocess
import traceback
import requests
from requests.exceptions import RequestException
import re
import os
# import difflib
# import errno

from terraflow.libraries.constants import *
from terraflow.libraries.helpers import *

# For this new setup, there should be a `.terraflow` folder added
# to each project.  Inside that folder should be a schemas folder
# and a docs folder where those artifacts can be cached.

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
    Get the current Terraform version from the terraform block.
    """
    try:
        result = subprocess.run(['terraform', 'version'], capture_output=True, text=True)
        output = result.stdout.strip()
        # Extracting the version information from the output
        version = output.split('\n')[0].split(' ')[-1].replace('v', '')
        return version
    except FileNotFoundError:
        # Handle the case where Terraform is not installed or not in the system's PATH
        return "Terraform command not found"
    except Exception as e:
        # Handle any other exceptions that might occur during the execution
        return f"Error occurred: {str(e)}"

# version = get_terraform_version()
# valid_versions = get_terraform_versions()
# print(is_valid_version(version, valid_versions))

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
