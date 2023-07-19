# import os
# import json
# import subprocess
# import traceback

# from terraflow.libraries.constants import *
# from terraflow.libraries.helpers import *

# # Schema functions.

# def get_schema(filename: str = f'{TERRAFLOW_DIR}/schema.json', cache: bool = True, refresh: bool = False) -> dict:
#     """
#     Returns the schema for a provider as a dictionary.

#     Args:
#         filename: The optional filename of the schema JSON file.
#         refresh: Flag indicating whether to refresh the schema if it already exists.

#     Returns:
#         The schema dictionary.
#     """
#     # Create the .terraflow directory if it doesn't already exist
#     if not os.path.exists(TERRAFLOW_DIR):
#         os.makedirs(TERRAFLOW_DIR)

#     # Get the schema from file if it exists and no refresh is requested
#     if filename and os.path.exists(filename) and not refresh:
#         schema = read_json_file(filename)
#         print(f'\n{colors("OK_BLUE")}Info:{colors()} Reading provider schema from cache.\n')
#     else:
#         schema = fetch_schema()
#         cache_schema(schema=schema)
#         print(f'\n{colors("OK_GREEN")}Success:{colors()} Schema downloaded successfully.\n')

#     return schema

# def fetch_schema() -> dict:
#     """
#     Gets a provider schema from Terraform.

#     Returns:
#         The schema dictionary fetched from Terraform.
#     """
#     try:
#         p = subprocess.run(["terraform", "init"], capture_output=True, text=True)
#         return json.loads(subprocess.check_output(["terraform", "providers", "schema", "-json"]).decode("utf-8"))
#     except subprocess.CalledProcessError:
#         print(
#             f'\n{colors(color="WARNING")}Warning:{colors()} The provider versions for this configuration have changed. Running an upgrade.\n'
#         )
#         p = subprocess.run(["terraform", "init", "-upgrade"], capture_output=True, text=True)
#         return json.loads(subprocess.check_output(["terraform", "providers", "schema", "-json"]).decode("utf-8"))

# def cache_schema(schema: dict = None, filename: str = ".terraflow/schema.json") -> None:
#     """
#     Cache the downloaded Terraform schema as ".terraflow/schema.json".

#     Args:
#         schema: The schema dictionary to be cached.
#         filename: The filename to save the schema as.
#     """
#     _, ext = os.path.splitext(filename)
#     if ext.lower() != ".json":
#         print(f'\n{colors("FAIL")}Error:{colors()} {filename} is not a JSON file.\n')
#         return

#     dirname = os.path.dirname(filename)
#     if not os.path.exists(dirname):
#         os.makedirs(dirname)

#     try:
#         if schema is None:
#             schema = get_schema(filename=filename, refresh=True)
#         write_json_file(filename, schema)
#         print(f'\n{colors("OK_GREEN")}Success:{colors()} Schema downloaded successfully.\n')
#     except Exception as e:
#         print(f'\n{colors("FAIL")}Error:{colors()} An error occurred while caching the schema: {traceback.format_exc()}\n')

# def get_provider_schema(schema: dict, namespace: str, provider: str) -> dict:
#     """
#     Get the schema for a given provider.

#     Args:
#         schema: The schema dictionary.
#         namespace: The provider's namespace.
#         provider: The provider name.

#     Returns:
#         The schema for the given provider.
#     """
#     return schema["provider_schemas"][f"{TERRAFORM_REGISTRY_BASE}/{namespace}/{provider}"]["provider"]

# def get_resource_schema(schema: dict, namespace: str, provider: str, resource: str) -> dict:
#     """
#     Get the schema for a given provider resource.

#     Args:
#         schema: The schema dictionary.
#         namespace: The provider's namespace.
#         provider: The provider name.
#         resource: The resource name.

#     Returns:
#         The schema for the given provider resource.
#     """
#     # Allow resource shorthand without the provider
#     if resource and provider not in resource:
#         resource = f"{provider}_{resource}"

#     return schema["provider_schemas"][f"{TERRAFORM_REGISTRY_BASE}/{namespace}/{provider}"]["resource_schemas"][resource]

# def get_data_schema(schema: dict, namespace: str, provider: str, data_source: str) -> dict:
#     """
#     Get the schema for a given provider data source.

#     Args:
#         schema: The schema dictionary.
#         namespace: The provider's namespace.
#         provider: The provider name.
#         data_source: The data source name.

#     Returns:
#         The schema for the given provider data source.
#     """
#     # Allow data source shorthand without the provider
#     if data_source and provider not in data_source:
#         data_source = f"{provider}_{data_source}"

#     return schema["provider_schemas"][f"{TERRAFORM_REGISTRY_BASE}/{namespace}/{provider}"]["data_source_schemas"][data_source]

# def get_attribute_schema(resource_schema: dict, blocks: list = None, attribute: str = None) -> dict:
#     """
#     Get the schema for a given provider, resource, or data source attribute.

#     Args:
#         resource_schema: The resource schema as a dictionary.
#         blocks: The list of blocks to traverse.
#         attribute: The attribute name.

#     Returns:
#         The schema for the given attribute.
#     """
#     try:
#         if blocks:
#             # Loop over all blocks in the blocks list
#             for block in blocks:
#                 # Go down into blocks until desired block is found
#                 resource_schema = resource_schema["block"]["block_types"].get(block, None)

#         return resource_schema["block"]["attributes"].get(attribute, None)
#     except Exception:
#         print(f'Error while trying to get the attribute schema: {traceback.format_exc()}')

# # import os
# # import json
# # import subprocess
# # import traceback

# # from terraflow.libraries.constants import *
# # from terraflow.libraries.helpers import *

# # class Schema:
# #     def __init__(self, filename: str = '.terraflow/schema.json', cache: bool = True, refresh: bool = False):
# #         self.filename = filename
# #         self.cache = cache
# #         self.schema = self.get_schema(refresh=refresh)

# #     def get_schema(self, refresh: bool = False) -> dict:
# #         if not os.path.exists(TERRAFLOW_DIR):
# #             os.makedirs(TERRAFLOW_DIR)

# #         if self.filename and os.path.exists(self.filename) and not refresh:
# #             schema = read_json_file(self.filename)
# #             print(f'\n{colors("OK_BLUE")}Info:{colors()} Reading provider schema from cache.\n')
# #         else:
# #             schema = self.fetch_schema()
# #             self.cache_schema(schema=schema)
# #             print(f'\n{colors("OK_GREEN")}Success:{colors()} Schema downloaded successfully.\n')

# #         return schema

# #     def fetch_schema(self) -> dict:
# #         try:
# #             p = subprocess.run(["terraform", "init"], capture_output=True, text=True)
# #             return json.loads(subprocess.check_output(["terraform", "providers", "schema", "-json"]).decode("utf-8"))
# #         except subprocess.CalledProcessError:
# #             print(
# #                 f'\n{colors(color="WARNING")}Warning:{colors()} The provider versions for this configuration have changed. Running an upgrade.\n'
# #             )
# #             p = subprocess.run(["terraform", "init", "-upgrade"], capture_output=True, text=True)
# #             return json.loads(subprocess.check_output(["terraform", "providers", "schema", "-json"]).decode("utf-8"))

# #     def cache_schema(self, schema: dict = None) -> None:
# #         _, ext = os.path.splitext(self.filename)
# #         if ext.lower() != ".json":
# #             print(f'\n{colors("FAIL")}Error:{colors()} {self.filename} is not a JSON file.\n')
# #             return

# #         dirname = os.path.dirname(self.filename)
# #         if not os.path.exists(dirname):
# #             os.makedirs(dirname)

# #         try:
# #             if schema is None:
# #                 schema = self.get_schema(refresh=True)
# #             write_json_file(self.filename, schema)
# #             print(f'\n{colors("OK_GREEN")}Success:{colors()} Schema downloaded successfully.\n')
# #         except Exception as e:
# #             print(f'\n{colors("FAIL")}Error:{colors()} An error occurred while caching the schema: {traceback.format_exc()}\n')

# #     def get_provider_schema(self, namespace: str, provider: str) -> dict:
# #         return self.schema["provider_schemas"][f"{TERRAFORM_REGISTRY_BASE}/{namespace}/{provider}"]["provider"]

# #     def get_resource_schema(self, namespace: str, provider: str, resource: str) -> dict:
# #         if resource and provider not in resource:
# #             resource = f"{provider}_{resource}"

# #         return self.schema["provider_schemas"][f"{TERRAFORM_REGISTRY_BASE}/{namespace}/{provider}"]["resource_schemas"][resource]

# #     def get_data_schema(self, namespace: str, provider: str, data_source: str) -> dict:
# #         if data_source and provider not in data_source:
# #             data_source = f"{provider}_{data_source}"

# #         return self.schema["provider_schemas"][f"{TERRAFORM_REGISTRY_BASE}/{namespace}/{provider}"]["data_source_schemas"][data_source]

# #     def get_attribute_schema(self, resource_schema: dict, blocks: list = None, attribute: str = None) -> dict:
# #         try:
# #             if blocks:
# #                 for block in blocks:
# #                     resource_schema = resource_schema["block"]["block_types"].get(block, None)

# #             return resource_schema["block"]["attributes"].get(attribute, None)
# #         except Exception:
# #             print(f'Error while trying to get the attribute schema: {traceback.format_exc()}')

# #     def enrich_schema(self, docs, schema=None, block_hierarchy=None):
# #         """
# #         Enriches the schema by adding descriptions to each attribute based on provided documentation.
# #         """
# #         # Initialize parameters if they were not provided
# #         if schema is None:
# #             schema = self.schema
# #         if block_hierarchy is None:
# #             block_hierarchy = []

# #         # Collect attributes and blocks in the current block
# #         attributes = schema.get("block", {}).get("attributes", {})
# #         blocks = schema.get("block", {}).get("block_types", {})

# #         # Loop through attributes
# #         for attribute, attribute_schema in attributes.items():
# #             # Get the description from the documentation
# #             attribute_description = get_resource_attribute_description(docs, attribute, block_hierarchy)

# #             # Update the attribute schema with the description
# #             attribute_schema['description'] = attribute_description

# #         # Loop through blocks
# #         for block, block_schema in blocks.items():
# #             updated_block_hierarchy = block_hierarchy + [block]

# #             # Recursive call to handle nested blocks
# #             self.enrich_schema(
# #                 docs=docs,
# #                 schema=block_schema,
# #                 block_hierarchy=updated_block_hierarchy
# #             )

# #         return schema

# # schema = Schema()
# # print(schema.schema)

import os
import json
import subprocess
import traceback

from terraflow.libraries.constants import *
from terraflow.libraries.helpers import *


class Schema:
    def __init__(self, filename: str = '.terraflow/schema.json', cache: bool = True, refresh: bool = False):
        self.filename = filename
        self.cache = cache
        self.refresh = refresh
        self.schema = self.get_schema()

    def get_schema(self):
        if not os.path.exists(TERRAFLOW_DIR):
            os.makedirs(TERRAFLOW_DIR)

        if self.filename and os.path.exists(self.filename) and not self.refresh:
            schema = read_json_file(self.filename)
            print(f'\n{colors("OK_BLUE")}Info:{colors()} Reading provider schema from cache.\n')
        else:
            schema = self.fetch_schema()
            self.cache_schema(schema=schema)
            print(f'\n{colors("OK_GREEN")}Success:{colors()} Schema downloaded successfully.\n')

        return schema

    def fetch_schema(self):
        try:
            p = subprocess.run(["terraform", "init"], capture_output=True, text=True)
            return json.loads(subprocess.check_output(["terraform", "providers", "schema", "-json"]).decode("utf-8"))
        except subprocess.CalledProcessError:
            print(
                f'\n{colors(color="WARNING")}Warning:{colors()} The provider versions for this configuration have changed. Running an upgrade.\n'
            )
            p = subprocess.run(["terraform", "init", "-upgrade"], capture_output=True, text=True)
            return json.loads(subprocess.check_output(["terraform", "providers", "schema", "-json"]).decode("utf-8"))

    def cache_schema(self, schema=None):
        _, ext = os.path.splitext(self.filename)
        if ext.lower() != ".json":
            print(f'\n{colors("FAIL")}Error:{colors()} {self.filename} is not a JSON file.\n')
            return

        dirname = os.path.dirname(self.filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        try:
            if schema is None:
                schema = self.get_schema(filename=self.filename, refresh=True)
            write_json_file(self.filename, schema)
            print(f'\n{colors("OK_GREEN")}Success:{colors()} Schema downloaded successfully.\n')
        except Exception as e:
            print(f'\n{colors("FAIL")}Error:{colors()} An error occurred while caching the schema: {traceback.format_exc()}\n')

    def get_provider_schema(self, namespace, provider):
        return self.schema["provider_schemas"][f"{TERRAFORM_REGISTRY_BASE}/{namespace}/{provider}"]["provider"]

    def get_resource_schema(self, namespace, provider, resource):
        if resource and provider not in resource:
            resource = f"{provider}_{resource}"

        return self.schema["provider_schemas"][f"{TERRAFORM_REGISTRY_BASE}/{namespace}/{provider}"]["resource_schemas"][resource]

    def get_data_schema(self, namespace, provider, data_source):
        if data_source and provider not in data_source:
            data_source = f"{provider}_{data_source}"

        return self.schema["provider_schemas"][f"{TERRAFORM_REGISTRY_BASE}/{namespace}/{provider}"]["data_source_schemas"][data_source]

    def get_attribute_schema(self, resource_schema, blocks=None, attribute=None):
        try:
            if blocks:
                for block in blocks:
                    resource_schema = resource_schema["block"]["block_types"].get(block, None)

            return resource_schema["block"]["attributes"].get(attribute, None)
        except Exception:
            print(f'Error while trying to get the attribute schema: {traceback.format_exc()}')

# schema = Schema(refresh=True)
# print(schema.schema)