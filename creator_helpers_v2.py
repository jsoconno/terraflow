import json
from pathlib import Path
import subprocess
import requests
from bs4 import BeautifulSoup
import re

class TerraformProvider:
    def __init__(self, namespace, provider, version, resource_type, resource_name='main', configuration_file_name='main.tf', variable_file_name='variables.tf', required_attributes_only=False, required_blocks_only=False, overwrite_code=False, format_code=True, add_descriptions=True, ignore_blocks=[], ignore_attributes=[], attribute_defaults={}, variable_prefix=None):
        # Make sure there is a provider configuration.
        try:
            # Initialize Terraform
            p = subprocess.run(['terraform', 'init', '-backend=false'], capture_output=True, text=True)
            if "Terraform initialized in an empty directory!" in p.stdout:
                raise Exception()
        except:
            # Create file that contains provider version details
            with open('ignore.tf', 'w') as f:
                f.write(f'terraform {{\n  required_providers {{\n    {provider} = {{\n      source = "{namespace}/{provider}"\n      version = "{version}"\n    }}\n  }}\n}}')
            # Initialize Terraform
            p = subprocess.run(['terraform', 'init', '-backend=false'])

        # Collect provider schema
        provider_schema_text = subprocess.check_output(['terraform', 'providers', 'schema', '-json']).decode("utf-8")
        
        self.namespace = namespace
        self.provider = provider
        self.version = version
        self.schema = json.loads(provider_schema_text)
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.configuration_file_name = configuration_file_name
        self.variable_file_name = variable_file_name
        self.required_attributes_only = required_attributes_only
        self.required_blocks_only = required_blocks_only
        self.overwrite_code = overwrite_code
        self.format_code = format_code
        self.add_descriptions = add_descriptions
        self.ignore_blocks = ignore_blocks
        self.ignore_attributes = ignore_attributes
        self.attribute_defaults = attribute_defaults
        self.variable_prefix = variable_prefix

    def _get_resource(self, resource_type):
        return self.schema['provider_schemas'][f'registry.terraform.io/{self.namespace}/{self.provider}']['resource_schemas'][resource_type]

    def _get_data_source(self, resource_type):
        return self.schema['provider_schemas'][f'registry.terraform.io/{self.namespace}/{self.provider}']['data_source_schemas'][resource_type]

    def _recurse_attributes(self, resource_schema, level=0, current_block='root', block_list=[], total_blocks=0, current_block_number=0, is_last_block=False):
        lines = []
        for k, v in resource_schema.items():
            if k == 'block':
                level += 1
                if current_block != 'root':
                    block_list.append(current_block)
                print(block_list)
                if 'attributes' in v:
                    attributes = v['attributes']
                    for attribute in attributes:

                        attribute_required = attributes[attribute].get("required", False)
                        print(attribute_required)

                        if 'required' in attributes[attribute]:
                            attribute_required = True
                        elif 'optional' in attributes[attribute]:
                            attribute_required = False
                        else:
                            attribute_required = None
                        
                        if self.variable_prefix:
                            variable_name = '_'.join([self.variable_prefix] + block_list + [attribute])
                        else:
                            variable_name = '_'.join(block_list + [attribute])

                        print(block_list[-1:])

                        if variable_name in self.ignore_attributes:
                            if attribute_required:
                                print(f'The attribute {attribute} was not excluded from the {self.resource_type} resource because it is required.')
                            else:
                                continue

                        attribute_description = attributes[attribute].get("description", None)
                        attribute_type = attributes[attribute].get("type", "string")

                        # Set attribute value
                        if attribute in self.attribute_defaults:
                            attribute_default = f'"{self.attribute_defaults[attribute]}"'
                        else:
                            attribute_default = f'var.{variable_name}'
                        
                        # Write attributes based on whether or not they are required
                        if attribute_required:
                            line = f'{level * "  "}{attribute} = {attribute_default}'      
                        elif not attribute_required and not self.required_attributes_only:
                            line = f'{level * "  "}{attribute} = {attribute_default}'
                        
                        if attribute_description and self.add_descriptions:
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

                        if current_block in self.ignore_blocks:
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
                        child_lines = self._recurse_attributes(v, level, current_block, block_list, total_blocks, current_block_number, is_last_block)
                        lines.extend(child_lines)
                        del block_list[-1:]
                    block_list = []
                
                # else:
        # This statement controls closing brackets
        level = level - 1
        line = f'{level * "  "}}}'
        lines.append(line)
        # if not current_block == 'root' and current_block_number == total_blocks:
        #     line = f'{(level - 1) * "  "}}}'
        #     lines.append(line)

        return lines

    def write_code(self):
        resource_schema = self._get_resource(self.resource_type)

        # Write header
        lines = [f'resource "{self.resource_type}" "{self.resource_name}" {{']

        # Write attributes
        body_lines = self._recurse_attributes(
            resource_schema=resource_schema
        )
        lines.extend(body_lines)

        text = '\n'.join(lines)

        if self.overwrite_code == True:
            write_mode = "w+"
        else:
            write_mode = "a+"

        with open(self.configuration_file_name, write_mode) as f:
            f.write(text)

        if self.format_code:
            p = subprocess.run(['terraform', 'fmt'])

        return text

def get_provider_resource_attribute_description(namespace, provider, resource, attribute, category="resources", block=None):
    url = f'https://registry.terraform.io/v1/providers/{namespace}/{provider}'
    response = json.loads(requests.get(url).text)

    docs_path = None
    
    for doc in response["docs"]:
        if doc["title"] == resource and doc["category"] == category:
            docs_path = doc["path"]

    if docs_path:
        docs_url = f'https://github.com/{namespace}/terraform-provider-{provider}/blob/main/{docs_path}'

        html_text = requests.get(docs_url).content.decode()
        documentation = ''.join(BeautifulSoup(html_text, features="html.parser").findAll(string=True))

        documentation = [line for line in documentation.split('\n') if line.strip() != '']

        # block_found = False
        # for line in documentation:
        #     if block:

        #     else
        #         if f'{attribute} -' in line:
        #             description = line

        if block:
            description = next(line for line in documentation if line.startswith(f'{attribute} -') and block in line.lower())
        else:
            description = next(line for line in documentation if line.startswith(f'{attribute} -'))
    
    else:
        description = ""

    return description


class Provider():

    def __init__(self, name, namespace='hashicorp', version=None):
        """
        Initialize inputs.
        """
        self.namespace = namespace
        self.name = name
        self.version = self._get_version(version)
        self._get_schema()
        self.schema = json.loads(subprocess.check_output(['terraform', 'providers', 'schema', '-json']).decode("utf-8"))

    def __repr__(self):
        return str({"namespace": self.namespace, "provider": self.name, "version": self.version})

    def get_dict(self):
        return {"namespace": self.namespace, "provider": self.name, "version": self.version}

    def _get_version(self, version):
        if version:
            if version in self.get_versions():
                version = version
            else:
                raise Exception(f'{self.version} is not a valid version.')
        else:
            version = self.get_latest_version()

        return version
    
    def get_versions(self):
        """
        Gets a list of versions for a given terraform provider such as aws, gcp, or azurerm.
        """
        versions = []

        response = requests.get(f"https://registry.terraform.io/v1/providers/{self.namespace}/{self.name}/versions")
        data = json.loads(response.text)

        for version in data["versions"]:
            versions.append(version["version"])

        versions = self._sort_versions(versions)
        
        return versions

    def get_semantic_version(self, version):
        """
        Get a dictionary of the semantic version components including major, minor, patch, and pre-release.
        """
        regex_pattern = r'(\d+)\.*(\d+)*\.*(\d+)*(?:-*(?:(?:[a-zA-Z]*(\d*)))?)'

        try:
            version = re.findall(regex_pattern, version)[0]
            version = tuple([int(component) for component in version if component != ''])

            # This block is used to standardize all version tuples so that
            # pre-releases are not prioritized above regular releases.
            version_length = len(version)
            missing_version_components = 4-version_length

            if 4-len(version) > 0:
                # Adding the version length at the end is used for pessimistic constraint operator logic.
                version = version + (0,)*(missing_version_components-1) + (1000000000000000,) + (version_length,)
        except:
            version = None

        return version

    def _sort_versions(self, versions, reverse=True):
        """
        Sorts lists of versions based on the semantic version.  Normal sort does not work because of versions like 1.67.0 vs. 1.9.0.
        """
        # print(versions)
        tuple_versions = [self.get_semantic_version(version) for version in versions]
        # print(tuple_versions)
        versions = [x for _, x in sorted(zip(tuple_versions, versions), reverse=reverse)]

        return versions

    def get_latest_version(self):
        """
        Provides the latest version based on a list of provided versions.
        """
        versions = versions = self.get_versions()

        if versions:
            latest_version = versions[0]
        else:
            latest_version = None

        return latest_version

    def create_terraform_code(self):
        """
        Create a Terraform provider file if one does not exist.
        """
        # Create file that contains provider version details
        with open('terraform-ai.tf', 'a+') as f:
            f.write(f'terraform {{\n  required_providers {{\n    {self.name} = {{\n      source = "{self.namespace}/{self.name}"\n      version = "{self.version}"\n    }}\n  }}\n}}')

    def _get_schema(self):
        """
        Get the schema for a provider.
        """
        try:
            # Initialize Terraform
            p = subprocess.run(['terraform', 'init', '-reconfigure', '-backend=false'], capture_output=True, text=True)
            
            # Determine if Terraform initialized in an empty directory
            if "Terraform initialized in an empty directory!" in p.stdout:
                raise Exception()
        except:
            # Create file that contains provider version details
            self.create_terraform_code()

            # Initialize Terraform
            p = subprocess.run(['terraform', 'init', '-backend=false'])

class Resource():
    def __init__(self):
        """
        Initialize inputs.
        """
        pass

    def get_resource_schema():
        """
        Get the schema for a provider resource.
        """

# print(get_provider_resource_attribute_description("hashicorp", "azurerm", "linux_function_app", "type", "data-sources", "connection_string"))

provider = Provider(
    namespace='hashicorp',
    name='azurerm',
    # version='3.44.0'
)

# print(provider.schema)