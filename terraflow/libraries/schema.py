import os
import json
import subprocess
import traceback

from terraflow.libraries.constants import *
from terraflow.libraries.helpers import *

# Schema functions.

def get_schema(filename: str = 'schema.json') -> dict:
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

def get_attribute_schema(resource_schema: dict, blocks: list = None, attribute: str = None) -> dict:
    """
    Get the schema for a given provider, resource, or data source attribute.

    Args:
        resource_schema: The resource schema as a dictionary.
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
                resource_schema = resource_schema["block"]["block_types"].get(block, None)

        return resource_schema["block"]["attributes"].get(attribute, None)
    except Exception:
        print(f'Error while trying to get the attribute schema: {traceback.format_exc()}')
