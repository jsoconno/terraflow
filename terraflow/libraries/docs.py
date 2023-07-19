import os
import re

from terraflow.libraries.constants import DOCUMENTATION_DIR, GITHUB_BASE
from terraflow.libraries.helpers import scrape_website, get_resource_attribute_description, parse_variables
from terraflow.libraries.schema import get_schema, get_resource_schema, get_data_schema, get_provider_schema
from terraflow.libraries.formatting import format_attribute_type

class TerraformDocumentation:
    def __init__(self, namespace, provider, version='main', kind=None, type=None, use_cache=True, refresh=False):
        self.namespace = namespace
        self.provider = provider
        self.version = version
        self.kind = kind
        self.type = type
        self.use_cache = use_cache
        self.refresh = refresh

        self.url = self._get_docs_url()
        self.text = self._get_docs_text()
        self.inputs = self._get_attributes(
            self.text,
            patterns=[
                r'^Argument(?:s)? Reference([\s\S]*?)^Attribute(?:s)? Reference',
                r'^Timeout(?:s)?([\s\S]*?)^Import'
            ]
        )
        self.outputs = self._get_attributes(
            self.text,
            patterns=[r'^Attribute(?:s)? Reference([\s\S]*?)^(?:Import|Timeouts)']
        )
        if self.type == 'provider':
            schema = get_provider_schema(get_schema(), self.namespace, self.provider)
        if self.type == 'resource':
            schema = get_resource_schema(get_schema(), self.namespace, self.provider, self.kind)
        elif self.type == 'data':
            schema = get_data_schema(get_schema(), self.namespace, self.provider, self.kind)
        self.metadata = self._get_attribute_metadata(schema)

    def _get_docs_url(self):
        if self.type == 'provider':
            return f"https://{GITHUB_BASE}/{self.namespace}/terraform-provider-{self.provider}/blob/{'' if self.version == 'main' else 'v'}{self.version}/website/docs/index.html.markdown"
        elif self.type == 'resource':
            return f"https://{GITHUB_BASE}/{self.namespace}/terraform-provider-{self.provider}/blob/{'' if self.version == 'main' else 'v'}{self.version}/website/docs/r/{self.kind}.html.markdown"
        elif self.type == 'data':
            return f"https://{GITHUB_BASE}/{self.namespace}/terraform-provider-{self.provider}/blob/{'' if self.version == 'main' else 'v'}{self.version}/website/docs/d/{self.kind}.html.markdown"
        else:
            raise ValueError("Invalid scope. Must be one of 'provider', 'resource', or 'data'.")
        
    def _get_docs_text(self):
        # Check is the user wants to use cache documentation
        if self.use_cache:
            # Set the documentation directory
            documentation_dir = os.path.join(DOCUMENTATION_DIR, self.namespace, self.provider, self.version)

            # Set the filepath
            if self.type == 'provider':
                filepath = os.path.join(documentation_dir)
            else:
                filepath = os.path.join(documentation_dir, self.kind)
            
            # Determine if the documentation directory exists, and if not, create it
            if not os.path.exists(filepath):
                os.makedirs(filepath)

            # If the file exists
            if os.path.exists(filepath + f'/{self.type}.txt'):
                # If refresh is True
                if self.refresh:
                    # Srape the documentation and write it to file
                    text = scrape_website(self.url, tag='article')
                    with open(filepath + f'/{self.type}.txt', 'w') as f:
                        f.write(text)
                        return text
                else:
                    # Read the existing documentation from file
                    with open(filepath + f'/{self.type}.txt', 'r') as f:
                        text = f.read()
                        return text
            else:
                # Srape the documentation and write it to file
                text = scrape_website(self.url, tag='article')
                with open(filepath + f'/{self.type}.txt', 'w') as f:
                    f.write(text)
                    return text

        else:
            # Srape the documentation and write it to file
            text = scrape_website(self.url, tag='article')
            return text
        
    def _get_attributes(self, documentation, patterns):
        sections = []
        for pattern in patterns:
            matches = re.findall(pattern, documentation, re.MULTILINE)
            if matches:
                sections.extend(matches)

        if sections:
            attributes = []
            attribute_pattern = r"`([\w_]+)` -"
            for section in sections:
                attribute_references = re.findall(attribute_pattern, section)
                for attribute_name in attribute_references:
                    attributes.append(attribute_name)
            
            return list(set(attributes))

        return []
    
    def _get_attribute_metadata(self, schema: dict, attribute_metadata: dict = None, block_hierarchy: list = None):
        """
        Writes the main body of the Terraform code using provided schema.
        """
        if attribute_metadata is None:
            attribute_metadata = {}
        
        if block_hierarchy is None:
            block_hierarchy = []

        # Collect attributes and blocks in the current block
        attributes = schema.get("block", {}).get("attributes", {})
        blocks = schema.get("block", {}).get("block_types", {})

        # Loop through attributes
        for attribute, attribute_schema in attributes.items():
            # Create ID
            id = '.'.join(block_hierarchy + [attribute])

            # Get the description from the documentation
            attribute_description = get_resource_attribute_description(self.text, attribute, block_hierarchy)

            # Write docs
            attribute_metadata[id] = {
                'name': attribute,
                'block_hierarchy': block_hierarchy,
                'input': True if attribute in self.inputs else False,
                'output': True if attribute in self.outputs else False,
                'required': attribute_schema.get('required', False),
                'optional': attribute_schema.get('optional', False),
                'type': format_attribute_type(attribute_schema.get('type')),
                'description': attribute_description,
                'metadata': attribute_schema
            }

        # Loop through blocks
        for block, block_schema in blocks.items():
            updated_block_hierarchy = block_hierarchy + [block]

            self._get_attribute_metadata(
                schema=block_schema,
                attribute_metadata=attribute_metadata,
                block_hierarchy=updated_block_hierarchy,
            )

        return attribute_metadata
    
# docs = TerraformDocumentation('hashicorp', 'azurerm', version='3.45.0', kind='resource_group', type='resource', use_cache=True, refresh=True)
# print(docs.outputs)
