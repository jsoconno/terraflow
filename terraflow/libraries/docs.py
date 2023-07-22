import os

from .constants import DOCUMENTATION_DIR, GITHUB_BASE
from .helpers import scrape_website, get_resource_attribute_description
from .schema import Schema
from .formatting import format_attribute_type

class TerraformDocumentation:
    def __init__(self, schema, namespace, provider, version='main', kind=None, type=None, use_cache=True, refresh=False):
        self.schema = schema
        self.namespace = namespace
        self.provider = provider
        self.version = version
        self.kind = kind
        self.type = type
        self.use_cache = use_cache
        self.refresh = refresh

        self.url = self._get_docs_url()
        self.text = self._get_docs_text()

        schema_data = self._get_schema_data()
        self.metadata = self._get_attribute_metadata(schema_data)

    def _get_schema_data(self):
        if self.type == 'provider':
            return self.schema.get_provider_schema(self.namespace, self.provider)
        elif self.type == 'resource':
            return self.schema.get_resource_schema(self.namespace, self.provider, self.kind)
        elif self.type == 'data':
            return self.schema.get_data_schema(self.namespace, self.provider, self.kind)
        else:
            raise ValueError("Invalid type. Must be one of 'provider', 'resource', or 'data'.")

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
            if os.path.exists(filepath + f'/{self.type}.md'):
                # If refresh is True
                if self.refresh:
                    # Srape the documentation and write it to file
                    text = scrape_website(self.url, tag='article')
                    with open(filepath + f'/{self.type}.md', 'w') as f:
                        f.write(text)
                        return text
                else:
                    # Read the existing documentation from file
                    with open(filepath + f'/{self.type}.md', 'r') as f:
                        text = f.read()
                        return text
            else:
                # Srape the documentation and write it to file
                text = scrape_website(self.url, tag='article')
                with open(filepath + f'/{self.type}.md', 'w') as f:
                    f.write(text)
                    return text

        else:
            # Srape the documentation and write it to file
            text = scrape_website(self.url, tag='article')
            return text
        
    @property
    def inputs(self):
        # return {k: v for k, v in self.metadata.items() if v['input']}
        return [k for k, v in self.metadata.items() if v['input']]

    @property
    def outputs(self):
        # return {k: v for k, v in self.metadata.items() if v['output']}
        return [k for k, v in self.metadata.items() if v['output']]

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

            # Set variables
            is_required = attribute_schema.get('required', False)
            is_optional = attribute_schema.get('optional', False)
            is_output = True if (not is_required and not is_optional) or id == 'id' else False
            is_input = not is_output
            formatted_type = format_attribute_type(attribute_schema.get('type'))

            #TODO: Remove this commented print statement
            # print(f'id: {id}, is_required: {is_required}, is_optional: {is_optional}, is_output: {is_output}, is_input: {is_input}')

            # Write docs
            attribute_metadata[id] = {
                'name': attribute,
                'block_hierarchy': block_hierarchy,
                'input': is_input,
                'output': is_output,
                'required': is_required,
                'optional': is_optional,
                'type': formatted_type,
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

# schema = Schema()
# docs = TerraformDocumentation(schema, 'hashicorp', 'azurerm', version='3.45.0', kind='windows_virtual_machine', type='resource', use_cache=True, refresh=True)
# print(docs.text)