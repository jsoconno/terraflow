from dataclasses import asdict
import re
import os

# from terraflow.libraries.schema import get_schema, get_provider_schema, get_resource_schema, get_data_schema
from .schema import Schema
from .helpers import (
    get_terraform_documentation_url,
    get_terraform_documentation,
    get_provider_version,
    get_terraform_version,
    filter_attributes,
    filter_blocks,
)
from .formatting import (
    format_attribute,
    format_block_header,
    format_resource_header,
    format_terraform_code,
)
from .configuration import (
    Configuration,
    ProviderConfiguration,
    ResourceConfiguration,
    DataSourceConfiguration,
    VariableConfiguration,
    OutputConfiguration,
)
from .docs import TerraformDocumentation
from .constants import VALID_TYPES


class CodeLoader:
    """
    Class responsible for loading and parsing Terraform code files.
    """

    def __init__(self, file_extensions: list = [".tf"]):
        self.file_extensions = file_extensions
        self.code = ""
        self.components = self._extract_components()

    def _read_file(self, file_name: str) -> str:
        """
        Read a file and return its content as a string.
        """
        with open(file_name, "r") as file:
            content = file.read() + "\n"
        self.code += content
        return content

    def _extract_components(self):
        # Store each component and its corresponding details
        components = []

        # Loop through all files with the provided extensions in the current directory
        for file_name in os.listdir(os.getcwd()):
            if any(file_name.endswith(extension) for extension in self.file_extensions):
                content = self._read_file(file_name)

                # Extract all Terraform components
                pattern = (
                    rf'((?:#.*\n)*?^(.*?)\s+(?:"(.*?)"\s+)?\s?"(.*?)"\s+{{[\s\S]*?^}}$)'
                )
                matches = re.findall(pattern, content, re.MULTILINE)

                for match in matches:
                    component = {
                        "id": f'{match[1]}.{match[2] + "." if match[2] else ""}{match[3]}',
                        "code": match[0],
                        "type": match[1],
                        "kind": match[2] if match[2] else None,
                        "name": match[3],
                        "filename": file_name,
                    }
                    components.append(component)

        return components

    def get_components(self, type: str = None, kind: str = None, name: str = None):
        """
        Return a list of components that match the provided type, kind, and/or name.

        Args:
            type (str, optional): The type of the component (e.g., 'resource', 'variable'). Defaults to None.
            kind (str, optional): The kind of the component (e.g., 'azurerm_resource_group'). Defaults to None.
            name (str, optional): The name of the component. Defaults to None.

        Returns:
            List[Dict]: A list of components matching the provided criteria.
        """
        filtered_components = self.components

        if type is not None:
            filtered_components = [
                comp for comp in filtered_components if comp["type"] == type
            ]

        if kind is not None:
            filtered_components = [
                comp for comp in filtered_components if comp["kind"] == kind
            ]

        if name is not None:
            filtered_components = [
                comp for comp in filtered_components if comp["name"] == name
            ]

        return filtered_components

    def get_component_id_list(self):
        """
        Return a list of component ids.

        Returns:
            List[str]: A list of component ids.
        """
        return [component["id"] for component in self.components]

    # TODO: Determine if it makes more sense to get components by id or by type, kind, and name
    def get_component_by_id(self, id):
        """
        Return a specific component by its id.

        Args:
            id (str): The id of the component.

        Returns:
            Dict: The component that matches the provided id or None if no match is found.
        """
        for component in self.components:
            if component["id"] == id:
                return component

        return None


# code = CodeLoader()
# print(code.get_components())


class CodeGenerator:
    """
    Base class representing a Terraform component.
    This class provides methods to generate Terraform code.
    """

    def __init__(self, provider: str, schema: Schema, namespace: str = "hashicorp"):
        self.namespace = namespace
        self.provider = provider
        self.kind = None
        self.type = "terraform"
        self.configuration = Configuration()
        self.code = ""
        self.schema = schema
        self.schema_json = schema.json
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
        code = ""

        if block_hierarchy is None:
            block_hierarchy = []

        # Get the documentation once and use it throughout the method
        if docs is None:
            docs = TerraformDocumentation(
                schema=self.schema,
                namespace=self.namespace,
                provider=self.provider,
                version=self.provider_version,
                kind=self.kind,
                type=self.type,
            ).metadata

        # Collect attributes and blocks in the current block
        attributes = schema.get("block", {}).get("attributes", {})
        blocks = schema.get("block", {}).get("block_types", {})

        # Apply filtering based on configuration
        attributes = filter_attributes(
            attributes=attributes,
            attribute_docs=docs,
            configuration=self.configuration,
            block_hierarchy=block_hierarchy,
        )
        blocks = filter_blocks(
            blocks=blocks,
            configuration=self.configuration,
            block_hierarchy=block_hierarchy,
        )

        # Loop through attributes
        for attribute, attribute_schema in attributes.items():
            # Create ID
            id = ".".join(block_hierarchy + [attribute])

            # Write line
            code += format_attribute(
                attribute=attribute,
                attribute_schema=attribute_schema,
                attribute_description=docs.get(id, {}).get("description", None),
                block_hierarchy=block_hierarchy,
                configuration=self.configuration,
            )

        # Loop through blocks
        for block, block_schema in blocks.items():
            updated_block_hierarchy = block_hierarchy + [block]

            header, footer = format_block_header(
                schema=block_schema,
                block=block,
                block_hierarchy=updated_block_hierarchy,
            )
            code += header
            # Recursive call to handle nested blocks
            code += self._write_body_code(
                schema=block_schema, docs=docs, block_hierarchy=updated_block_hierarchy
            )
            code += footer

        return code

    def _write_code(self, schema: dict):
        """
        Generates the terraform code for a specific type.
        """
        code = ""

        header, footer = format_resource_header(
            type=self.type,
            name=self.name,
            provider=self.provider,
            kind=self.kind,
            documentation_url=(
                self.docs_url
                if self.configuration.add_header_terraform_docs_url
                else None
            ),
            comment=(self.configuration.header_comment),
        )

        # Write code
        code += header
        code += self._write_body_code(schema)
        code += footer

        # Format code
        code = format_terraform_code(code)

        return code

    @property
    def docs_url(self):
        return get_terraform_documentation_url(
            type=self.type,
            namespace=self.namespace,
            provider=self.provider,
            resource=self.kind,
            version=self.provider_version,
        )

    @property
    def docs(self):
        return get_terraform_documentation(
            namespace=self.namespace,
            provider=self.provider,
            scope=self.type,
            resource=self.kind,
            version=self.provider_version,
        )

    @property
    def provider_version(self):
        return get_provider_version(self.provider, self.namespace)

    @property
    def terraform_version(self):
        return get_terraform_version()


class ProviderComponent(CodeGenerator):
    """
    Class representing a Terraform provider.
    """

    def __init__(
        self,
        name: str,
        schema: Schema,
        namespace: str = "hashicorp",
        configuration: ProviderConfiguration = None,
    ):
        super().__init__(name, schema, namespace)
        self.name = name
        self.type = "provider"
        self.schema_json = schema.get_provider_schema(
            namespace=namespace, provider=name
        )
        self.configuration = (
            configuration if configuration is not None else ProviderConfiguration()
        )
        self.code = self._write_code(self.schema_json)


class ResourceComponent(CodeGenerator):
    """
    Class representing a Terraform resource.
    """

    def __init__(
        self,
        kind: str,
        provider: str,
        schema: Schema,
        name: str = "main",
        namespace: str = "hashicorp",
        configuration: ResourceConfiguration = None,
    ):
        super().__init__(provider, schema, namespace)
        # Set initial variables
        self.name = name
        self.type = "resource"
        self.kind = kind
        self.schema_json = schema.get_resource_schema(
            namespace=namespace, provider=provider, resource=kind
        )

        self.configuration = (
            configuration if configuration is not None else ResourceConfiguration()
        )
        self.code = self._write_code(self.schema_json)


class DataSourceComponent(CodeGenerator):
    """
    Class representing a Terraform data source.
    """

    def __init__(
        self,
        kind: str,
        provider: str,
        schema: Schema,
        name: str = "main",
        namespace: str = "hashicorp",
        configuration: DataSourceConfiguration = None,
    ):
        super().__init__(provider, schema, namespace)
        # Set initial variables
        self.name = name
        self.type = "data"
        self.kind = kind
        self.schema_json = schema.get_data_schema(
            namespace=namespace, provider=provider, data_source=kind
        )
        self.configuration = (
            configuration if configuration is not None else DataSourceConfiguration()
        )
        self.code = self._write_code(self.schema_json)


class VariableComponent:
    """
    Class representing a Terraform variable.
    """

    # def _validate_type(self, variable_type: str):
    #     # Check if the normalized type is in the set of valid types
    #     if variable_type not in VALID_TYPES:
    #         print(f"The type '{variable_type}' is not a valid Terraform variable type.")
    #     # For complex types, further validation logic can be added here
    #     return variable_type

    def __init__(
        self,
        name: str,
        kind: str,
        schema: Schema,
        provider: str,
        namespace: str = "hashicorp",
        default=None,
        description: str = None,
        variable_type: str = None,
        configuration: VariableConfiguration = None,
    ):
        self.name = name
        self.default = default
        self.description = description
        self.variable_type = variable_type  # self._validate_type(variable_type)  # Ensure the variable type is in lowercase to match Terraform syntax
        self.configuration = (
            configuration if configuration is not None else VariableConfiguration()
        )
        self.kind = kind

        # If a description is not provided, fetch it using the schema and provider information
        terraform_documentation = TerraformDocumentation(
            schema=schema,
            namespace=namespace,
            provider=provider,
            kind=self.kind,
            version=get_provider_version(provider, namespace),
            type="resource",  # TODO: Can I make this a variable?
        )

        self.docs = terraform_documentation.metadata
        self.description = (
            terraform_documentation.metadata.get(name, {}).get(
                "description", f"Default description for {name}"
            )
            if not description
            else description
        )

        self.code = self._write_code()

    def _write_code(self):
        """
        Generates the Terraform code for a variable.
        """
        code = f'variable "{self.name}" {{\n'
        if self.variable_type == None:
            code += f'  type = {self.docs[self.name].get("type")}\n'
        else:
            code += f"  type = {self.variable_type}\n"
        if self.description:
            code += f'  description = "{self.description}"\n'
        if self.default is not None:
            # Format the default value based on the type provided by the user
            if self.variable_type == "string":
                # Only add quotes for string types
                code += f'  default = "{self.default}"\n'
            else:
                # For non-string types, output the default value as is
                code += f"  default = {self.default.lower()}\n"
        code += "}\n"
        return code


# Usage example
# variable = VariableComponent(name="instance_size", default="t2.micro", description="The size of the instance", variable_type="string")
# print(variable.code)

# schema = Schema()

# config = ResourceConfiguration(
#     add_inline_descriptions=True,
#     exclude_blocks=['timeouts'],
#     add_header_terraform_docs_url=True,
#     attribute_value_prefix="test",
#     attribute_defaults={'location': 'eastus'},
#     header_comment='This key vault is used for storing keys, secrets, and certificates for the application.'
# )

# x = ResourceComponent(
#     namespace='hashicorp',
#     provider='azurerm',
#     schema=schema,
#     kind='key_vault',
#     name='test',
#     configuration=config
# )

# print(x.code)

# x._write_variables_code()

# configuration = ProviderConfiguration(
#     add_inline_descriptions=True
# )

# provider = ProviderComponent(
#     name='azurerm',
#     configuration=configuration
# )

# print(provider.code)
