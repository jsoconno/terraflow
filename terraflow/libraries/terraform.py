from dataclasses import asdict
import re
import os

# from terraflow.libraries.schema import get_schema, get_provider_schema, get_resource_schema, get_data_schema
from terraflow.libraries.schema import Schema
from terraflow.libraries.helpers import (
    get_provider_version,
    get_terraform_version,
    filter_attributes,
    filter_blocks,
)
from terraflow.libraries.formatting import (
    format_attribute,
    format_block_header,
    format_resource_header,
    format_terraform_code,
)
from terraflow.libraries.configuration import (
    Configuration,
    ProviderConfiguration,
    ResourceConfiguration,
    DataSourceConfiguration,
    VariableConfiguration,
    OutputConfiguration,
)
from terraflow.libraries.docs import TerraformDocumentation
from terraflow.libraries.constants import VALID_TYPES


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


class TerraformBase:
    """
    Base class for all Terraform objects.
    """

    def __init__(
        self,
        schema: Schema,
        namespace: str,
        provider: str,
        provider_version: str = None,
        type: str = None,
        name: str = None,
        kind: str = None,
        configuration: Configuration = None,
    ):
        self.schema = schema
        self.terraform_version = get_terraform_version()
        self.namespace = namespace
        self.provider = provider
        self.provider_version = (
            provider_version
            if provider_version
            else get_provider_version(self.provider, self.namespace)
        )
        self.kind = kind
        self.type = type
        self.name = name
        self.configuration = configuration if configuration else Configuration()

        self.code = ""
        self.documentation = TerraformDocumentation(
            schema=self.schema,
            namespace=self.namespace,
            provider=self.provider,
            version=self.provider_version,
            kind=self.kind,
            type=self.type,
        )


class TerraformCodeMixin:
    """
    Class responsible for generating Terraform code.
    """

    def _write_body_code(self, schema: dict, docs=None, block_hierarchy: list = None):
        """
        Writes the main body of the Terraform code using provided schema.
        """
        code = ""

        if block_hierarchy is None:
            block_hierarchy = []

        # Collect attributes and blocks in the current block
        attributes = schema.get("block", {}).get("attributes", {})
        blocks = schema.get("block", {}).get("block_types", {})

        # Apply filtering based on configuration
        attributes = filter_attributes(
            attributes=attributes,
            attribute_docs=self.documentation.metadata,
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
                attribute_description=self.documentation.metadata.get(id, {}).get(
                    "description", None
                ),
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
                schema=block_schema,
                docs=self.documentation.metadata,
                block_hierarchy=updated_block_hierarchy,
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
                self.documentation.url
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


class TerraformProvider(TerraformBase, TerraformCodeMixin):
    def __init__(
        self,
        schema: Schema,
        namespace: str,
        provider: str,
        provider_version: str = None,
        type: str = "provider",
        name: str = None,
        kind: str = None,
        configuration: ProviderConfiguration = None,
    ):
        super().__init__(
            schema,
            namespace,
            provider,
            provider_version,
            type,
            name,
            kind,
            configuration,
        )

        provider_schema = self.schema.get_provider_schema(
            namespace=self.namespace,
            provider=self.provider,
        )
        self.code = self._write_code(schema=provider_schema)
        self.configuration = configuration if configuration else ProviderConfiguration()


class TerraformResource(TerraformBase, TerraformCodeMixin):
    def __init__(
        self,
        schema: Schema,
        namespace: str,
        provider: str,
        kind: str,
        provider_version: str = None,
        type: str = "resource",
        name: str = "main",
        configuration: ResourceConfiguration = None,
    ):
        super().__init__(
            schema,
            namespace,
            provider,
            provider_version,
            type,
            name,
            kind,
            configuration,
        )

        resource_schema = self.schema.get_resource_schema(
            namespace=self.namespace,
            provider=self.provider,
            resource=self.kind,
        )
        self.code = self._write_code(schema=resource_schema)
        self.configuration = configuration if configuration else ResourceConfiguration()


class TerraformDataSource(TerraformBase, TerraformCodeMixin):
    def __init__(
        self,
        schema: Schema,
        namespace: str,
        provider: str,
        provider_version: str,
        kind: str,
        type: str = "data",
        name: str = "main",
        configuration: DataSourceConfiguration = None,
    ):
        super().__init__(
            schema,
            namespace,
            provider,
            provider_version,
            type,
            name,
            kind,
            configuration,
        )

        data_source_schema = self.schema.get_data_schema(
            namespace=self.namespace,
            provider=self.provider,
            data_source=self.kind,
        )
        self.code = self._write_code(schema=data_source_schema)
        self.configuration = (
            configuration if configuration else DataSourceConfiguration()
        )


class TerraformVariable(TerraformBase):
    def __init__(
        self,
        schema: Schema,
        namespace: str,
        provider: str,
        kind: str,
        name: str,
        type: str,
        provider_version: str = None,
        variable_type: str = None,
        configuration: VariableConfiguration = None,
        default=None,
        description: str = None,
    ):
        super().__init__(
            schema,
            namespace,
            provider,
            provider_version,
            type,
            name,
            kind,
            configuration,
        )

        self.name = name
        self.kind = kind
        self.default = default
        self.description = (
            self.documentation.metadata.get(name, {}).get(
                "description", f"Default description for {name}"
            )
            if not description
            else description
        )
        self.type = type
        self.variable_type = variable_type

        self.configuration = configuration if configuration else VariableConfiguration()
        self.code = self._write_code()

    def _write_code(self):
        """
        Generates the Terraform code for a variable.
        """
        code = f'variable "{self.name}" {{\n'
        if self.variable_type == None:
            code += f'  type = {self.documentation.metadata[self.name].get("type")}\n'
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


# schema = Schema()
# configuration = ResourceConfiguration(
#     exclude_attributes=["tags"], exclude_blocks=["timeouts"]
# )

# terraform = TerraformResource(
#     schema=schema,
#     namespace="hashicorp",
#     provider="azurerm",
#     kind="resource_group",
#     name="name",
#     type="resource",
#     # provider_version="3.45.0",
#     configuration=configuration,
# )

# print(terraform.code)
