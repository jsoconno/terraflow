from dataclasses import asdict

from terraflow.libraries.schema import get_schema, get_provider_schema, get_resource_schema, get_data_source_schema, get_attribute_schema
from terraflow.libraries.helpers import get_terraform_documentation_url, get_terraform_documentation, get_resource_attribute_description, format_attribute_type
from terraflow.libraries.configuration import ProviderConfiguration, ResourceConfiguration, DataSourceConfiguration, VariableConfiguration, OutputConfiguration

class Terraform:
    def __init__(self, provider, namespace="hashicorp"):
        self.provider = provider
        self.namespace = namespace
        self.content = ""
        self.config = {}

    def write_line(self, line):
        self.content += line

    def add_resource_wrapper(self, header, documentation_url=None, comment=None):
        header_content = ""

        if documentation_url:
            header_content += f"# Terraform docs: {documentation_url}\n"

        if comment:
            wrapped_comment = "\n".join(["# " + line for line in wrap_text(text=comment)])
            header_content += f"{wrapped_comment}\n"

        header_content += f"{header}\n"
        footer = "}\n"

        return header_content, footer

class Block(Terraform):
    def __init__(self, provider, namespace="hashicorp"):
        super().__init__(provider, namespace)
        self.variables = {}
        self.outputs = {}
        self.code = ""
        self.variables_text = ""
        self.outputs_text = ""

        # Load the documentation at initialization
        self.documentation_url = ""
        self.documentation_text = ""

    def add_variable(self, variable_name, variable_type, description, optional):  # Copy this method from the Variable class
        if variable_name not in self.variables:
            default_value = 'null' if optional else ''
            self.variables[variable_name] = {
                'type': variable_type,
                'description': description,
                'default': default_value
            }

    def add_output(self, output_name, description, depends_on=None):
        self.outputs[output_name] = {
            'description': description,
            'depends_on': depends_on or []
        }

    def add_attribute(self, attribute, attribute_schema, block_hierarchy=[]):
        # Get attribute description from the pre-loaded documentation
        if isinstance(self, Provider) and self.config.get('add_description', False):
            description = attribute_schema.get('description', '')
        else:
            description = ""
            if self.documentation_text and self.config.get('add_description', False):
                description = get_resource_attribute_description(self.documentation_text, attribute, block_hierarchy)

        # Construct the attribute name
        if block_hierarchy:
            attribute_name = "_".join(block_hierarchy + [attribute])
        else:
            attribute_name = attribute

        if description:
            attribute_content = f"{attribute} = var.{attribute_name} # {description}\n"
        else:
            attribute_content = f"{attribute} = var.{attribute_name}\n"

        # Add variable when you add an attribute
        if attribute_schema:
            variable_type = attribute_schema.get('type')
            optional = attribute_schema.get('optional', False)
            self.add_variable(attribute_name, variable_type, description, optional)
        
        self.write_line(attribute_content)

    def write_variables_code(self, schema=None, block_hierarchy=[]):
        if schema is None:
            schema = self.get_schema()
        
        variables_text = ""
        attributes = schema.get("block", {}).get("attributes", {})
        blocks = schema.get("block", {}).get("block_types", {})

        for attribute, attribute_schema in attributes.items():
            # Construct the attribute name
            if block_hierarchy:
                attribute_name = "_".join(block_hierarchy + [attribute])
            else:
                attribute_name = attribute

            if attribute_name in self.variables:
                properties = self.variables[attribute_name]
                variables_text += f'variable "{attribute_name}" {{\n'
                variables_text += f'type = {format_attribute_type(properties["type"])}\n'
                if self.config.get('add_description', False) and self.documentation_text:
                    description = get_resource_attribute_description(self.documentation_text, attribute, block_hierarchy)
                else:
                    description = properties["description"]
                if description:
                    variables_text += f'description = "{description}"\n'
                if properties['default']:
                    variables_text += f'default = {properties["default"]}\n'
                variables_text += '}\n\n'
            
        for block, block_schema in blocks.items():
            variables_text += self.write_variables_code(schema=block_schema, block_hierarchy=block_hierarchy + [block])
            
        return variables_text

    def write_outputs_code(self, schema=None, block_hierarchy=[]):
        if schema is None:
            schema = self.get_schema()

        outputs_text = ""
        attributes = schema.get("block", {}).get("attributes", {})
        blocks = schema.get("block", {}).get("block_types", {})

        for attribute, attribute_schema in attributes.items():
            # Construct the attribute name
            if block_hierarchy:
                attribute_name = "_".join(block_hierarchy + [attribute])
            else:
                attribute_name = attribute

            outputs_text += f'output "{attribute_name}" {{\n'
            # standardize resource and data source attribute so we can remove some of this logic
            if isinstance(self, Resource):
                outputs_text += f'value = {self.provider}_{self.resource}.{self.name}.{".".join(block_hierarchy + [attribute])}\n'
            if isinstance(self, DataSource):
                outputs_text += f'value = {self.provider}_{self.data_source}.{self.name}.{".".join(block_hierarchy + [attribute])}\n'
            # TODO: Fix the description functionality
            description = ""
            if self.config.get('add_description', False) and self.documentation_text:
                description = get_resource_attribute_description(self.documentation_text, attribute, block_hierarchy)
            if description:
                outputs_text += f'description = "{description}"\n'
            outputs_text += '}\n\n'
            
        for block, block_schema in blocks.items():
            outputs_text += self.write_outputs_code(schema=block_schema, block_hierarchy=block_hierarchy + [block])
            
        return outputs_text

    def add_block_wrapper(self, schema, block, block_hierarchy):
        header = ""
        # Simplify the condition check for required blocks
        if schema.get("min_items", 0) > 0:
            required_blocks_message = "required"
        else:
            required_blocks_message = "optional"

        header += f"\n# This block is {required_blocks_message}\n"
        header += f"{block} {{\n"
        footer = "}\n"

        return header, footer

    def write_code(self, schema, block_hierarchy=[]):
        attributes = schema.get("block", {}).get("attributes", {})
        blocks = schema.get("block", {}).get("block_types", {})

        for attribute, attribute_schema in attributes.items():
            self.add_attribute(attribute, attribute_schema, block_hierarchy)

        for block, block_schema in blocks.items():
            block_header, block_footer = self.add_block_wrapper(block_schema, block, block_hierarchy)
            self.write_line(block_header)
            # Recursive call to handle nested blocks
            self.write_code(block_schema, block_hierarchy + [block])
            self.write_line(block_footer)

    def get_code(self, config={}):
        self.config = config
        schema = self.get_schema()
        self.code = self.write_code(schema)

        return self.code

    def get_variables(self, config={}):
        self.config = config
        schema = self.get_schema()
        self.variables_text = self.write_variables_code(schema)

        return self.variables_text

    def get_outputs(self, config={}):
        self.config = config
        schema = self.get_schema()
        self.outputs_text = self.write_outputs_code(schema=schema)

        return self.outputs_text

class Provider(Block):
    def __init__(self, provider, namespace="hashicorp"):
        super().__init__(provider, namespace)
        self.code = self.get_code()
        self.variables_text = self.get_variables()

    def get_schema(self):
        schema = get_schema()
        provider_schema = get_provider_schema(schema=schema, namespace=self.namespace, provider=self.provider)

        return provider_schema

    def write_provider_code(self, schema):
        header = f'provider "{self.provider}" {{\n'
        footer = "}\n"
        self.write_line(header)
        self.write_code(schema)
        self.write_line(footer)

    def get_code(self, config={}):
        self.config = config
        schema = self.get_schema()
        self.write_provider_code(schema=schema)
        
        return self.content

class Resource(Block):
    def __init__(self, provider, resource, name="main", namespace="hashicorp"):
        super().__init__(provider, namespace)
        self.resource = resource
        self.name = name

        # Load the documentation at initialization
        self.documentation_url = get_terraform_documentation_url(self.namespace, self.provider, 'resource', self.resource)
        self.documentation_text = get_terraform_documentation(self.namespace, self.provider, 'resource', self.resource)

        self.code = self.get_code()

    def get_schema(self):
        schema = get_schema()
        resource_schema = get_resource_schema(schema=schema, namespace=self.namespace, provider=self.provider, resource=self.resource)

        return resource_schema

    def write_resource_code(self, schema, name):
        header = f'resource "{self.provider}_{self.resource}" "{name}" {{\n'
        footer = "}\n"
        self.write_line(header)
        self.write_code(schema)
        self.write_line(footer)

    def get_code(self, config={}):
        self.config = config
        schema = self.get_schema()
        self.write_resource_code(schema=schema, name=self.name)
        
        return self.content

class DataSource(Block):
    def __init__(self, provider, data_source, name="main", namespace="hashicorp"):
        super().__init__(provider, namespace)
        self.data_source = data_source
        self.name = name

        # Load the documentation at initialization
        self.documentation_url = get_terraform_documentation_url(self.namespace, self.provider, 'data_source', self.data_source)
        self.documentation_text = get_terraform_documentation(self.namespace, self.provider, 'data_source', self.data_source)

        self.code = self.get_code()
        self.variables_text = self.get_variables()

    def get_schema(self):
        schema = get_schema()
        data_source_schema = get_data_source_schema(schema=schema, namespace=self.namespace, provider=self.provider, data_source=self.data_source)

        return data_source_schema

    def write_data_source_code(self, schema, name):
        header = f'data "{self.provider}_{self.data_source}" "{name}" {{\n'
        footer = "}\n"
        self.write_line(header)
        self.write_code(schema)
        self.write_line(footer)

    def get_code(self, config={}):
        self.config = config
        schema = self.get_schema()
        self.write_data_source_code(schema=schema, name=self.name)
        
        return self.content

# Set configurations
config = ProviderConfiguration(add_description=False)
variable_config = VariableConfiguration(add_description=True)
output_config = OutputConfiguration(add_description=True)

# Create Provider code
# provider = Provider(provider="azurerm")
# print(provider.get_code(config=asdict(config)))
# print(provider.get_variables(config=asdict(variable_config)))
# print(provider.get_outputs(config=asdict(output_config)))

# Create Resource code
resource = Resource(provider="azurerm", resource="virtual_network", name="this")
# print(resource.get_code(config=asdict(config)))
# print(resource.get_variables(config=asdict(variable_config)))
# print(resource.get_outputs(config=asdict(output_config)))

# Create Data Source code
data_source = DataSource(provider="azurerm", data_source="virtual_network", name="this")
print(data_source.get_code(config=asdict(config)))
print(data_source.get_variables(config=asdict(variable_config)))
print(data_source.get_outputs(config=asdict(output_config)))