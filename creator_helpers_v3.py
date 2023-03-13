import json
from pathlib import Path
import subprocess
import requests
from bs4 import BeautifulSoup
import re
import os

class TerraformConfiguration():
    """
    A class for managing provider schemas.
    """
    def __init__(self, provider, resource=None, namespace='hashicorp'):
        """
        Collect the provider schema based on current configuration.
        """
        # Create the schema file
        try:
            full_schema = json.loads(subprocess.check_output(['terraform', 'providers', 'schema', '-json']).decode("utf-8"))
        except:
            subprocess.run(['terraform', 'init', '-upgrade'], capture_output=True, text=True)
            full_schema = json.loads(subprocess.check_output(['terraform', 'providers', 'schema', '-json']).decode("utf-8"))

        self.namespace = namespace
        self.provider = provider
        self.resource = resource
        self.full_schema = full_schema
        self.provider_schema = self.get_provider_schema()
        self.resource_schema = self.get_resource_schema()

    def get_full_schema(self):
        """
        Returns the full schema for all providers as a dictionary.
        """
        return self.full_schema

    def get_provider_schema(self):
        """
        Returns the schema for a provider as a dictionary.
        """
        return self.full_schema['provider_schemas'].get(f'registry.terraform.io/{self.namespace}/{self.provider}', {})

    def get_provider_provider_schema(self):
        """
        Returns the schema for a provider as a dictionary.
        """
        return self.full_schema['provider_schemas'].get(f'registry.terraform.io/{self.namespace}/{self.provider}', {})

    def get_resource_schema(self):
        """
        Returns the schema for a resource as a dictionary.
        """
        return self.get_provider_schema()['resource_schemas'].get(self.resource, {})

    def get_resource_attribute_schema(self, attribute, blocks=None):
        """
        Returns the schema for a resource attribute as a dictionary.
        """
        resource_schema = self.get_resource_schema()

        # Set starting point for the attribute schema
        attribute_schema = resource_schema

        if blocks:
            # Loop over all blocks in the blocks list
            for block in blocks:
                # Go down into blocks until desired block is found
                attribute_schema = attribute_schema['block']['block_types'].get(block, None)

        attribute_schema = attribute_schema['block']['attributes'].get(attribute, None)

        return attribute_schema

    def get_resource_attribute_value(self, attribute, attribute_key, blocks=None, format_output=False):
        """
        Returns the schema for a resource attribute as a dictionary.
        """
        attribute_value = self.get_resource_attribute_schema(
            attribute=attribute,
            blocks=blocks
        )
        
        attribute_value = attribute_value.get(attribute_key, None)

        if format_output and attribute_key == 'type':
            attribute_value = self._format_attribute_type(attribute_value)

        return attribute_value

    def get_providers(self):
        """
        Returns an available list of providers based on the configuration.
        """
        providers = []

        try:
            provider_schemas = self.full_schema["provider_schemas"]
            for provider in provider_schemas:
                provider_components = provider.replace('registry.terraform.io/', '').split('/')
                providers.append({
                    "namespace": provider_components[0],
                    "provider": provider_components[1]
                })
        except:
            print('There are no available providers in the configuration.')

        return providers

    def get_resources(self):
        """
        Returns an available list of resources based on the configuration.
        """
        resources = []

        try:
            resource_schemas = self.get_provider_schema()['resource_schemas']
            for resource in resource_schemas:
                resources.append(resource)
        except:
            print('There are no available resources in the configuration.')

        return resources

    def download_full_schema(self, filename='full_schema'):
        with open(f'{filename}.json', 'w+') as f:
            f.write(json.dumps(self.full_schema))

    def download_provider_schema(self, filename='schema'):
        with open(f'{filename}.json', 'w+') as f:
            f.write(json.dumps(self.schema))

    def get_code(
        self,
        resource_schema={},
        level=0,
        current_block='root',
        block_list=[],
        total_blocks=0,
        current_block_number=0,
        is_last_block=False,
        resource_name='main',
        variable_file_name='variables.tf',
        required_attributes_only=False,
        required_blocks_only=False,
        add_descriptions=True,
        ignore_blocks=[],
        ignore_attributes=[],
        attribute_defaults={},
        variable_prefix=None
    ):
        # Set defaults
        lines = []
        if resource_schema == {}:
            resource_schema = self.resource_schema

        # Write header
        if current_block == 'root':
            lines = [f'resource "{self.resource}" "{resource_name}" {{']
        
        for k, v in resource_schema.items():
            if k == 'block':
                level += 1
                if current_block != 'root':
                    block_list.append(current_block)
                if 'attributes' in v:
                    attributes = v['attributes']
                    for attribute in attributes:
                        attribute_schema = self.get_resource_attribute_schema(attribute=attribute, blocks=block_list)
                        attribute_required = self._is_required_attribute(
                            attribute_metadata=attribute_schema
                        )
                        
                        variable_name = self._get_variable_name(
                            block_list=block_list,
                            attribute_name=attribute,
                            variable_prefix=variable_prefix
                        )

                        if variable_name in ignore_attributes:
                            if attribute_required:
                                print(f'The attribute {attribute} was not excluded from the {self.resource_type} resource because it is required.')
                            else:
                                continue

                        attribute_description = self.get_resource_attribute_value(attribute=attribute, attribute_key='description', blocks=block_list)
                        attribute_type = self.get_resource_attribute_value(attribute=attribute, attribute_key='type', blocks=block_list)

                        # Set attribute value
                        attribute_default = self._get_attribute_value(
                            attribute=attribute,
                            attribute_defaults=attribute_defaults,
                            attribute_value=variable_name
                        )
                        # print(f'{attribute}, {attribute_type}, {attribute_description}, {attribute_default}')

                        # Write attributes based on whether or not they are required
                        if attribute_required:
                            line = f'{level * "  "}{attribute} = {attribute_default}'      
                        elif not attribute_required and not required_attributes_only:
                            line = f'{level * "  "}{attribute} = {attribute_default}'
                        
                        if attribute_description and add_descriptions:
                            line = f'{line} # {attribute_description}'

                        lines.append(line)

                if 'block_types' in v:
                    current_block_number = 0
                    blocks = v['block_types']
                    for k, v in blocks.items():
                        current_block = k
                        if current_block == "email":
                            pass
                        block_min_items = v.get("min_items", None)
                        block_max_items = v.get("max_items", None)
                        
                        if block_min_items:
                            block_required = True
                        else:
                            block_required = False

                        if current_block in ignore_blocks:
                            if block_required:
                                print(f'The block {current_block} was not excluded from the {self.resource_type} resource because it is required.')
                            else:
                                continue

                        if block_max_items and block_max_items > 1:
                            multiple_blocks_allowed = True
                        else:
                            multiple_blocks_allowed = False

                        if block_required:
                            if multiple_blocks_allowed:
                                lines.append(f'\n{level * "  "}# This block is required and allows for up to {block_max_items} items.')
                            else:
                                lines.append(f'\n{level * "  "}# This block is required and allows only one item.')
                        else:
                            if multiple_blocks_allowed:
                                lines.append(f'\n{level * "  "}# This block is optional and allows for up to {block_max_items} items.')
                            else:
                                lines.append(f'\n{level * "  "}# This block is optional and allows only one item.')
                        
                        current_block_number += 1
                        total_blocks = len(blocks)
                        is_last_block = level == 1 and current_block_number == total_blocks
                        line = f'{level * "  "}{k} {{'
                        lines.append(line)
                        child_lines = self.get_code(v, level, current_block, block_list, total_blocks, current_block_number, is_last_block)
                        lines.append(child_lines)
                        del block_list[-1:]
                    block_list = []
                
        # This statement controls closing brackets
        level = level - 1
        line = f'{level * "  "}}}'
        lines.append(line)

        text = '\n'.join(lines)

        return text

    def _format_attribute_type(self, attribute_type):
        """
        Formats the data type for terraform variables.
        """
        if isinstance(attribute_type, str):
            return attribute_type
        elif isinstance(attribute_type, list):
            element_type = self._format_attribute_type(attribute_type[-1])
            for i in range(len(attribute_type) - 2, -1, -1):
                element_type = f"{attribute_type[i]}({element_type})"
            return element_type
        elif isinstance(attribute_type, dict):
            object_type = ""
            for key, value in attribute_type.items():
                object_type += f"{key} = {self._format_attribute_type(value)}\n"
            return f"object({{\n{object_type}}})"
        else:
            raise ValueError(f"Invalid Terraform data type: {attribute_type}")

    def _get_variable_name(self, block_list, attribute_name, variable_prefix=None):
        """
        Creates an attributes variable name based on the nesting of blocks and attributes name with an optional prefix.
        """
        if variable_prefix:
            variable_name = '_'.join([variable_prefix] + block_list + [attribute_name])
        else:
            variable_name = '_'.join(block_list + [attribute_name])

        return variable_name

    def _get_attribute_value(self, attribute, attribute_defaults, attribute_value):
        """
        Gets the attribute value to the variable name unless a default is provided.
        """
        # TODO: fix this so that nested items work as well.
        if attribute in attribute_defaults:
            attribute_default = attribute_defaults[attribute]
            if not '.' in attribute_default:
                attribute_default = f'"{attribute_default}"'
        else:
            attribute_default = f'var.{attribute_value}'

        return attribute_default

    def _is_required_attribute(self, attribute_metadata):
        """
        Determines whether or not an attribute is required.
        """
        if 'required' in attribute_metadata:
            result = True
        elif 'optional' in attribute_metadata:
            result = False
        else:
            result = None

        return result

class TerraformResource():
    """
    A class for managing the creation of Terraform resources.
    """
    def __init__(self, provider_schema, resource_type):
        self.provider_schema = provider_schema
        self.resource_type = resource_type
        self.schema = self.provider_schema['resource_schemas'].get(self.resource_type, {})

    def get_schema(self):
        return self.schema

    def _get_variable_name(self, block_list, attribute_name, variable_prefix=None):
        """
        Creates an attributes variable name based on the nesting of blocks and attributes name with an optional prefix.
        """
        if variable_prefix:
            variable_name = '_'.join([variable_prefix] + block_list + [attribute_name])
        else:
            variable_name = '_'.join(block_list + [attribute_name])

        return variable_name

    def _get_attribute_description(self, attribute_metadata):
        """
        Returns the description for an attribute.
        """
        description = attribute_metadata.get("description", None)

        return description

    def _get_attribute_type(self, attribute_metadata):
        """
        Returns the type for an attribute.
        """
        data_type = attribute_metadata.get("type", None)

        return data_type

    def _format_attribute_type(self, attribute_type):
        """
        Formats the data type for terraform variables.
        """
        if isinstance(attribute_type, str):
            return attribute_type
        elif isinstance(attribute_type, list):
            element_type = self._format_attribute_type(attribute_type[-1])
            for i in range(len(attribute_type) - 2, -1, -1):
                element_type = f"{attribute_type[i]}({element_type})"
            return element_type
        elif isinstance(attribute_type, dict):
            object_type = ""
            for key, value in attribute_type.items():
                object_type += f"{key} = {self._format_attribute_type(value)}\n"
            return f"object({{\n{object_type}}})"
        else:
            raise ValueError(f"Invalid Terraform data type: {attribute_type}")

    def _get_attribute_value(self, attribute, attribute_defaults, attribute_value):
        """
        Gets the attribute value to the variable name unless a default is provided.
        """
        # TODO: fix this so that nested items work as well.
        if attribute in attribute_defaults:
            attribute_default = attribute_defaults[attribute]
            if not '.' in attribute_default:
                attribute_default = f'"{attribute_default}"'
        else:
            attribute_default = f'var.{attribute_value}'

        return attribute_default

    def get_attribute_dynamic_reference(self, resource_type, attribute, resource_name='main'):
        """
        Returns the dynamic references for a given attribute.
        """
        return f'{resource_type}.{resource_name}.{attribute}'

    def _is_required_attribute(self, attribute_metadata):
        """
        Determines whether or not an attribute is required.
        """
        if 'required' in attribute_metadata:
            result = True
        elif 'optional' in attribute_metadata:
            result = False
        else:
            result = None

        return result

    def get_code(
        self,
        resource_schema,
        level=0,
        current_block='root',
        block_list=[],
        total_blocks=0,
        current_block_number=0,
        is_last_block=False,
        resource_name='main',
        variable_file_name='variables.tf',
        required_attributes_only=False,
        required_blocks_only=False,
        add_descriptions=True,
        ignore_blocks=[],
        ignore_attributes=[],
        attribute_defaults={},
        variable_prefix=None
    ):

        # Write header
        lines = []

        if current_block == 'root':
            lines = [f'resource "{self.resource_type}" "{resource_name}" {{']
        # lines.append(f'resource "{self.resource_type}" "{resource_name}" {{')
        
        for k, v in resource_schema.items():
            if k == 'block':
                level += 1
                if current_block != 'root':
                    block_list.append(current_block)
                if 'attributes' in v:
                    attributes = v['attributes']
                    for attribute in attributes:
                        attribute_required = self._is_required_attribute(attribute_metadata=attributes[attribute])
                        # if 'required' in attributes[attribute]:
                        #     attribute_required = True
                        # elif 'optional' in attributes[attribute]:
                        #     attribute_required = False
                        # else:
                        #     attribute_required = None
                        
                        variable_name = self._get_variable_name(
                            block_list=block_list,
                            attribute_name=attribute,
                            variable_prefix=variable_prefix
                        )
                        # if variable_prefix:
                        #     variable_name = '_'.join([variable_prefix] + block_list + [attribute])
                        # else:
                        #     variable_name = '_'.join(block_list + [attribute])

                        if variable_name in ignore_attributes:
                            if attribute_required:
                                print(f'The attribute {attribute} was not excluded from the {self.resource_type} resource because it is required.')
                            else:
                                continue

                        attribute_description = self._get_attribute_description(attribute_metadata=attributes[attribute])
                        attribute_type = self._get_attribute_type(attribute_metadata=attributes[attribute])
                        # attribute_description = attributes[attribute].get("description", None)
                        # attribute_type = attributes[attribute].get("type", "string")

                        # Set attribute value
                        attribute_default = self._get_attribute_value(
                            attribute=attribute,
                            attribute_defaults=attribute_defaults,
                            attribute_value=variable_name
                        )
                        # if attribute in attribute_defaults:
                        #     attribute_default = f'"{attribute_defaults[attribute]}"'
                        # else:
                        #     attribute_default = f'var.{variable_name}'

                        # Write attributes based on whether or not they are required
                        if attribute_required:
                            line = f'{level * "  "}{attribute} = {attribute_default}'      
                        elif not attribute_required and not required_attributes_only:
                            line = f'{level * "  "}{attribute} = {attribute_default}'
                        
                        if attribute_description and add_descriptions:
                            line = f'{line} # {attribute_description}'

                        lines.append(line)

                if 'block_types' in v:
                    current_block_number = 0
                    blocks = v['block_types']
                    for k, v in blocks.items():
                        current_block = k
                        if current_block == "email":
                            pass
                        block_min_items = v.get("min_items", None)
                        block_max_items = v.get("max_items", None)
                        
                        if block_min_items:
                            block_required = True
                        else:
                            block_required = False

                        if current_block in ignore_blocks:
                            if block_required:
                                print(f'The block {current_block} was not excluded from the {self.resource_type} resource because it is required.')
                            else:
                                continue

                        if block_max_items and block_max_items > 1:
                            multiple_blocks_allowed = True
                        else:
                            multiple_blocks_allowed = False

                        if block_required:
                            if multiple_blocks_allowed:
                                lines.append(f'\n{level * "  "}# This block is required and allows for up to {block_max_items} items.')
                            else:
                                lines.append(f'\n{level * "  "}# This block is required and allows only one item.')
                        else:
                            if multiple_blocks_allowed:
                                lines.append(f'\n{level * "  "}# This block is optional and allows for up to {block_max_items} items.')
                            else:
                                lines.append(f'\n{level * "  "}# This block is optional and allows only one item.')
                        
                        current_block_number += 1
                        total_blocks = len(blocks)
                        is_last_block = level == 1 and current_block_number == total_blocks
                        line = f'{level * "  "}{k} {{'
                        lines.append(line)
                        child_lines = self.get_code(v, level, current_block, block_list, total_blocks, current_block_number, is_last_block)
                        lines.append(child_lines)
                        del block_list[-1:]
                    block_list = []
                
        # This statement controls closing brackets
        level = level - 1
        line = f'{level * "  "}}}'
        lines.append(line)

        text = '\n'.join(lines)

        return text



resource = TerraformConfiguration(
    provider='azurerm',
    resource="azurerm_linux_function_app"
).get_code(
    attribute_defaults={'name': 'test'}
)

with open('main.tf', 'w+') as f:
    f.write(resource)


    # def write_code_2(self, resource_name='main'):
    #     # resource_schema = self.get_schema()

    #     # Write header
    #     lines = [f'resource "{self.resource_type}" "{resource_name}" {{']

    #     # Write attributes
    #     body_lines = self._recurse_attributes(
    #         resource_schema=resource_schema
    #     )
    #     lines.extend(body_lines)

    #     text = '\n'.join(lines)

    #     if self.overwrite_code == True:
    #         write_mode = "w+"
    #     else:
    #         write_mode = "a+"

    #     with open(self.configuration_file_name, write_mode) as f:
    #         f.write(text)

    #     if self.format_code:
    #         p = subprocess.run(['terraform', 'fmt'])

    #     return text


# provider = TerraformProvider(
#     namespace="hashicorp",
#     name="azurerm"
# )

# resource_group = TerraformResource(
#     provider_schema = provider.get_schema(),
#     resource_type = "azurerm_resource_group"
# )

# function_app = TerraformResource(
#     provider_schema = provider.get_schema(), 
#     resource_type = "azurerm_linux_function_app"
# )

# resource_group_code = resource_group.get_code(
#     resource_schema=resource_group.get_schema(),
#     attribute_defaults={"name": "test", "location": "eastus"}
# )

# function_app_code = function_app.get_code(
#     resource_schema=function_app.get_schema(),
#     attribute_defaults={"name": "test", "location": resource_group.get_attribute_dynamic_reference(resource_type=resource_group.resource_type, attribute="location")}
# )

# print(function_app_code)

# # def _get_attribute_type(data_type):
# #     """
# #     Returns the type for an attribute.
# #     """

# #     if isinstance(data_type, str):
# #         return data_type
# #     elif isinstance(data_type, list):
# #         element_type = _get_attribute_type(data_type[-1])
# #         for i in range(len(data_type) - 2, -1, -1):
# #             element_type = f"{data_type[i]}({element_type})"
# #         return element_type
# #     elif isinstance(data_type, dict):
# #         object_type = ""
# #         for key, value in data_type.items():
# #             object_type += f"{key} = {_get_attribute_type(value)}\n"
# #         return f"object({{\n{object_type}}})"
# #     else:
# #         raise ValueError(f"Invalid Terraform data type: {data_type}")

# # print(_get_attribute_type(data_type=['map', 'string']))

