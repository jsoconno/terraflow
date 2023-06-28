import re
import os
from terraflow.libraries.schema import get_schema, get_provider_schema, get_resource_schema, get_data_source_schema, get_attribute_schema
from terraflow.libraries.helpers import get_terraform_documentation_url, get_terraform_documentation, get_resource_attribute_description, format_attribute_type

class Terraform:
    def __init__(self, provider, namespace="hashicorp"):
        self.provider = provider
        self.namespace = namespace
        self.content = ""
        self.outputs = []
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
        self.code = ""
        self.variables_text = ""

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

    def add_attribute(self, attribute, attribute_schema, block_hierarchy=[]):
        # Get attribute description from the pre-loaded documentation
        if isinstance(self, Provider):
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
        self.variables_text = self.write_variables_code()
        return self.variables_text

class Provider(Block):
    def __init__(self, provider, namespace="hashicorp"):
        super().__init__(provider, namespace)
        self.code = self.get_code()
        # self.variables_text = self.get_variables()

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

provider = Provider(provider="azurerm")
print(provider.get_code())
print(provider.get_variables(config={'add_description': True}))


class Resource(Block):
    def __init__(self, provider, resource, namespace="hashicorp"):
        super().__init__(provider, namespace)
        self.resource = resource

        # Load the documentation at initialization
        self.documentation_url = get_terraform_documentation_url(self.namespace, self.provider, 'resource', self.resource)
        self.documentation_text = get_terraform_documentation(self.namespace, self.provider, 'resource', self.resource)

        self.code = self.get_code(name='main')

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

    def get_code(self, name='main', config={}):
        self.config = config
        schema = self.get_schema()
        self.write_resource_code(schema=schema, name=name)
        
        return self.content

# resource = Resource(provider="azurerm", resource="virtual_network")
# print(resource.get_code(name="my_virtual_network"))
# print(resource.get_variables(config={'add_description': True}))

class DataSource(Block):
    def __init__(self, provider, data_source, namespace="hashicorp"):
        super().__init__(provider, namespace)
        self.data_source = data_source

        # Load the documentation at initialization
        self.documentation_url = get_terraform_documentation_url(self.namespace, self.provider, 'data_source', self.data_source)
        self.documentation_text = get_terraform_documentation(self.namespace, self.provider, 'data_source', self.data_source)

        self.code = self.get_code(name='main')
        # self.variables_text = self.get_variables()

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

    def get_code(self, name='main', config={}):
        self.config = config
        schema = self.get_schema()
        self.write_data_source_code(schema=schema, name='main')
        
        return self.content
        
# data_source = DataSource(provider="azurerm", data_source="subnet")
# print(data_source.get_code(name="my_subnet", config={"add_description": False}))
# print(data_source.get_variables(config={'add_description': True}))











# class Variable(Block):
#     def __init__(self, namespace, provider, object_type, variable_names=None, variable_description=None, variable_type=None, variable_default=None):
#         super().__init__(provider, namespace)
#         self.object_type = object_type
#         self.variable_names = variable_names or []
#         if isinstance(self.variable_names, str):
#             self.variable_names = [self.variable_names]  # Convert to list if only one name is provided
#         self.variable_description = variable_description or ""
#         self.variable_type = variable_type or "any"
#         self.variable_default = variable_default or "null"
#         self.variables = {}

#         # Load the documentation at initialization
#         self.documentation_url = get_terraform_documentation_url(self.namespace, self.provider, 'resource', self.object_type)
#         self.documentation_text = get_terraform_documentation(self.namespace, self.provider, 'resource', self.object_type)
    
#     def add_variable(self, attribute_name, variable_name):
#         # Get the description if not provided
#         if not self.variable_description or len(self.variable_names) > 1:
#             self.variable_description = get_resource_attribute_description(
#                 self.documentation_text, attribute_name, block_hierarchy=[])

#         # Get the attribute schema
#         attribute_schema = get_attribute_schema(self.provider, blocks=None, attribute=attribute_name)

#         # Get and format the attribute type
#         if attribute_schema and "type" in attribute_schema:
#             attribute_type = format_attribute_type(attribute_schema["type"])
#             if not self.variable_type or len(self.variable_names) > 1:
#                 self.variable_type = attribute_type

#         variable_code = f'variable "{variable_name}" {{\ndescription = "{self.variable_description}"\ntype = {self.variable_type}'

#         # Check if "default" should be added
#         if "(Required)" not in self.variable_description:
#             variable_code += f'\ndefault = {self.variable_default}'
#         variable_code += '\n}}'

#         # Add the variable to the dictionary
#         self.variables[variable_name] = variable_code

#     def search_attributes(self, content):
#         # regex pattern to find attributes and variable pairs in content
#         pattern = r'\s*?(.*?)\s*?=\s*?var.(.*?)\s+\n?'
#         matches = re.findall(pattern, content, re.MULTILINE)

#         # Create Terraform variable for each match
#         for attribute, variable in matches:
#             attribute = attribute.strip()
#             variable = variable.strip()
#             # if specific variable is given, only add it
#             if self.variable_names and variable not in self.variable_names:
#                 continue
#             # avoid adding same variable twice
#             if variable not in self.variables:
#                 self.add_variable(attribute, variable)

#     def get_code(self):
#         content = ""
#         # Iterate over all .tf files in the current directory
#         for file_name in os.listdir(os.getcwd()):
#             if file_name.endswith('.tf'):
#                 with open(file_name, 'r') as tf_file:
#                     content += tf_file.read()

#         # Search attributes in the aggregated content
#         self.search_attributes(content)

#         return self.variables

# variable = Variable(namespace="hashicorp", provider="azurerm", object_type="key_vault", variable_names=["test_name"])
# variables = variable.get_code()
# print(variables)
