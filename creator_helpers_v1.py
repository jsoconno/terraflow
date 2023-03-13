import json
from pathlib import Path
import subprocess

class TerraformProvider:
    def __init__(self, namespace, provider, version):
        # Create file that contains provider version details
        with open('versions.tf', 'w') as f:
            f.write(f'terraform {{\n  required_providers {{\n    {provider} = {{\n      source = "{namespace}/{provider}"\n      version = "{version}"\n    }}\n  }}\n}}')
        
        # Initialize Terraform
        subprocess.run(['terraform', 'init', '-backend=false'])

        # Collect provider schema
        provider_schema_text = subprocess.check_output(['terraform', 'providers', 'schema', '-json']).decode("utf-8")
        
        self.namespace = namespace
        self.provider = provider
        self.version = version
        self.schema = json.loads(provider_schema_text)

    def _get_resource(self, resource_type):
        return self.schema['provider_schemas'][f'registry.terraform.io/{self.namespace}/{self.provider}']['resource_schemas'][resource_type]

    def _get_data_source(self, resource_type):
        return self.schema['provider_schemas'][f'registry.terraform.io/{self.namespace}/{self.provider}']['data_source_schemas'][resource_type]

    def _filter_attributes(self, resource_schema, required_attributes_only):
        for k, v in resource_schema.items():
            if k == 'block':
                attributes = v['attributes']
                for attribute in attributes:
                    if not 'required' in attributes[attribute]:
                        resource_schema.pop(k)
                        print(resource_schema)

                if 'block_types' in v:
                    blocks = v['block_types']
                    for k, v in blocks.items():
                        current_block = k
                        self._recurse_attributes(v, current_block)

    def _recurse_attributes(self, resource_schema, level=0, current_block='root', total_blocks=0, current_block_number=0, is_last_block=False):
        for k, v in resource_schema.items():
            if k == 'block':
                level += 1
                if 'attributes' in v:
                    attributes = v['attributes']
                    for attribute in attributes:
                        if not 'computed' in attributes[attribute]:
                            line = level * '  ' + attribute + ' = ' + 'var.' + attribute
                            print(line)

                if 'block_types' in v:
                    current_block_number = 0
                    blocks = v['block_types']
                    for k, v in blocks.items():
                        # parent_remaining_blocks = total_blocks - current_block_number
                        current_block = k
                        current_block_number += 1
                        total_blocks = len(blocks)
                        is_last_block = level == 1 and current_block_number == total_blocks
                        line = '\n' + level * '  ' + k + ' {'
                        print(line)
                        self._recurse_attributes(v, level, current_block, total_blocks, current_block_number, is_last_block)
                
                else:
                    # This statement controls closing brackets
                    level = level - 1
                    line = (level) * '  ' + '}'
                    print(line)
                    if not current_block == 'root' and current_block_number == total_blocks:
                        line = (level - 1) * '  ' + '}'
                        print(line)


    def write_resource(self, resource_type, resource_name="main", required_attributes_only=False, is_primary_resource=True):
        resource_schema = self._get_resource(resource_type)

        # Write header
        print(f'resource "{resource_type}" "{resource_name}" {{')

        # Write attributes
        self._recurse_attributes(resource_schema)

        # Write footer
        print('}')
        