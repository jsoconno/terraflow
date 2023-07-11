from dataclasses import asdict
import re

from terraflow.libraries.schema import get_schema, get_provider_schema, get_resource_schema, get_data_schema, get_attribute_schema
from terraflow.libraries.helpers import get_terraform_documentation_url, get_terraform_documentation, get_resource_attribute_description, handle_attribute, get_provider_version, get_terraform_version, filter_attributes, filter_blocks, read_files, load_terraform_code
from terraflow.libraries.formatting import format_attribute, format_block_header, format_resource_header, format_attribute_type, format_terraform_code
from terraflow.libraries.configuration import Configuration, ProviderConfiguration, ResourceConfiguration, DataSourceConfiguration, VariableConfiguration, OutputConfiguration

class Terraform():
    """
    Base class representing a Terraform entity.
    This class provides methods to generate Terraform code.
    """
    def __init__(self, provider: str, namespace: str = "hashicorp"):#, load_code: bool = False):
        self.namespace = namespace
        self.provider = provider
        self.kind = None
        self.type = 'terraform'
        self.configuration = Configuration()
        self.code = ''
        self.schema = get_schema()
        self.attributes = {}

    def _write_code_line(self, line: str):
        """
        Appends a line of code to the overall Terraform code.
        """
        self.code += line

    def _write_body_code(self, schema: dict, docs=None, block_hierarchy: list = None):
        """
        Writes the main body of the Terraform code using provided schema.
        """
        code = ''
        
        if block_hierarchy is None:
            block_hierarchy = []

        # Collect attributes and blocks in the current block
        attributes = schema.get("block", {}).get("attributes", {})
        blocks = schema.get("block", {}).get("block_types", {})

        # Apply filtering based on configuration
        attributes = filter_attributes(attributes=attributes, configuration=self.configuration)
        blocks = filter_blocks(blocks=blocks, configuration=self.configuration)

        # Get the documentation once and use it throughout the method
        if docs is None:
            docs = self.docs

        # Loop through attributes
        for attribute, attribute_schema in attributes.items():
            # Get the description from the documentation
            attribute_description = get_resource_attribute_description(docs, attribute, block_hierarchy)

            # Update the attribute schema with the description
            attribute_schema['description'] = attribute_description
            self.attributes.update({'_'.join(block_hierarchy + [attribute]): attribute_schema})

            # Write line
            code += format_attribute(
                attribute=attribute,
                attribute_schema=attribute_schema,
                attribute_description=attribute_description,
                block_hierarchy=block_hierarchy,
                configuration=self.configuration
            )

        # Loop through blocks
        for block, block_schema in blocks.items():
            updated_block_hierarchy = block_hierarchy + [block]

            header, footer = format_block_header(
                schema=block_schema,
                block=block,
                block_hierarchy=updated_block_hierarchy
            )
            code += header
            # Recursive call to handle nested blocks
            code += self._write_body_code(
                schema=block_schema,
                docs=docs,
                block_hierarchy=block_hierarchy + [block]
            ) + '\n'
            code += footer

        return code
    
    def _write_code(self, schema: dict):
        """
        Generates the terraform code for a specific type.
        """
        code = ''

        header, footer = format_resource_header(
            type=self.type,
            name=self.name,
            kind=self.kind,
            documentation_url=(self.docs_url if self.configuration.add_header_terraform_docs_url else None),
            comment=(self.configuration.header_comment)
        )

        # Write code
        code += header
        code += self._write_body_code(schema)
        code += footer

        # Format code
        code = format_terraform_code(code)

        return code

    # def _load_code(self):
    #     """
    #     Loop through all Terraform files in the current directory and load code of the current Terraform object.
    #     """
    #     terraform_code = read_files()
    #     load_terraform_code(
    #         type=self.type,
    #         kind=self.kind,
    #         name=self.name,
    #         code=terraform_code
    #     )

    @property
    def docs_url(self):
        return get_terraform_documentation_url(
            type=self.type,
            namespace=self.namespace,
            provider=self.provider,
            resource=self.kind,
            version=self.provider_version
        )

    @property
    def docs(self):
        return get_terraform_documentation(
            namespace=self.namespace,
            provider=self.provider,
            scope=self.type,
            resource=self.kind,
            version=self.provider_version
        )

    @property
    def provider_version(self):
        return get_provider_version(self.provider, self.namespace)

    @property
    def terraform_version(self):
        return get_terraform_version()

class Provider(Terraform):
    """
    Class representing a Terraform provider.
    """
    def __init__(self, name: str, namespace: str = 'hashicorp', configuration: ProviderConfiguration = None):#, load_code: bool = False):
        super().__init__(name, namespace)#, load_code)
        # Set initial variables
        self.name = name
        self.type = 'provider'
        self.schema = get_provider_schema(
            schema=self.schema,
            namespace=namespace,
            provider=name
        )
        self.configuration = configuration if configuration is not None else ProviderConfiguration()
        self.code = self._write_code(self.schema)
        # if load_code:
        #     self.code = self._load_code()
        # else:
        #     self.code = self._write_code(self.schema)

class Resource(Terraform):
    """
    Class representing a Terraform resource.
    """
    def __init__(self, kind: str, provider: str, name: str = 'main', namespace: str = 'hashicorp', configuration: ResourceConfiguration = None):#, load_code: bool = False):
        super().__init__(provider, namespace)#, load_code)
        # Set initial variables
        self.name = name
        self.type = 'resource'
        self.kind = kind
        self.schema = get_resource_schema(
            schema=self.schema,
            namespace=namespace,
            provider=provider,
            resource=kind
        )
        self.configuration = configuration if configuration is not None else ResourceConfiguration()
        self.code = self._write_code(self.schema)
        # if load_code:
        #     self.code = self._load_code()
        # else:
        #     self.code = self._write_code(self.schema)

class DataSource(Terraform):
    """
    Class representing a Terraform data source.
    """
    def __init__(self, kind: str, provider: str, name: str = 'main', namespace: str = 'hashicorp', configuration: DataSourceConfiguration = None):#, load_code: bool = False):
        super().__init__(provider, namespace)#, load_code)
        # Set initial variables
        self.name = name
        self.type = 'data'
        self.kind = kind
        self.schema = get_data_schema(
            schema=self.schema,
            namespace=namespace,
            provider=provider,
            data_source=kind
        )
        self.configuration = configuration if configuration is not None else DataSourceConfiguration()
        self.code = self._write_code(self.schema)
        # if load_code:
        #     self.code = self._load_code()
        # else:
        #     self.code = self._write_code(self.schema)

# config = ResourceConfiguration(
#     add_inline_descriptions=False,
#     exclude_blocks=['timeouts'],
#     add_header_terraform_docs_url=True,
#     attribute_value_prefix="test",
#     attribute_defaults={'location': 'eastus'},
#     header_comment='This key vault is used for storing keys, secrets, and certificates for the application.'
# )

# x = Resource(
#     namespace='hashicorp',
#     provider='azurerm',
#     kind='key_vault',
#     name='test',
#     configuration=config
# )

# print(x.code)