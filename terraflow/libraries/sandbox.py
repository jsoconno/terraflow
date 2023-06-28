import re
import os
from terraflow.libraries.schema import get_schema, get_provider_schema, get_resource_schema, get_data_source_schema, get_attribute_schema
from terraflow.libraries.helpers import get_terraform_documentation_url, get_terraform_documentation, get_resource_attribute_description

class TerraformGenerator:
    def __init__(self, provider, namespace="hashicorp", add_description=False):
        self.provider = provider
        self.namespace = namespace
        self.content = ""
        self.outputs = []
        self.add_description = add_description

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

class BlockGenerator(TerraformGenerator):
    def __init__(self, provider, namespace="hashicorp", add_description=False):
        super().__init__(provider, namespace, add_description)

    def add_attribute(self, attribute, attribute_schema, block_hierarchy=[]):
        # Get attribute description from the pre-loaded documentation
        description = ""
        if self.documentation_text and self.add_description:
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
        
        self.write_line(attribute_content)

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

class ProviderGenerator(BlockGenerator):
    def __init__(self, provider, namespace="hashicorp", add_description=False):
        super().__init__(provider, namespace, add_description)

    def write_provider_code(self, schema):
        header = f'provider "{self.provider}" {{\n'
        footer = "}\n"
        self.write_line(header)
        self.write_code(schema)
        self.write_line(footer)

    def generate(self, schema):
        self.write_provider_code(schema)
        print(self.content)

# # Use the classes
# provider_generator = ProviderGenerator("azurerm")
# schema = get_schema()
# provider_schema = get_provider_schema(schema, "hashicorp", "azurerm")
# provider_generator.generate(provider_schema)


class ResourceGenerator(BlockGenerator):
    def __init__(self, provider, resource_type, namespace="hashicorp", add_description=False):
        super().__init__(provider, namespace, add_description)
        self.resource_type = resource_type

        # Load the documentation at initialization
        self.documentation_url = get_terraform_documentation_url(self.namespace, self.provider, 'resource', self.resource_type)
        self.documentation_text = get_terraform_documentation(self.namespace, self.provider, 'resource', self.resource_type)

    def write_resource_code(self, resource_name, schema):
        header = f'resource "{self.provider}_{self.resource_type}" "{resource_name}" {{\n'
        footer = "}\n"
        self.write_line(header)
        self.write_code(schema)
        self.write_line(footer)

    def generate(self, resource_name, schema):
        self.write_resource_code(resource_name, schema)
        print(self.content)

resource_generator = ResourceGenerator("azurerm", "virtual_network")
schema = get_schema()
resource_schema = get_resource_schema(schema, "hashicorp", "azurerm", "virtual_network")
resource_generator.generate("my_virtual_network", resource_schema)

class DataSourceGenerator(BlockGenerator):
    def __init__(self, provider, data_source_type, namespace="hashicorp", add_description=False):
        super().__init__(provider, namespace, add_description)
        self.data_source_type = data_source_type

        # Load the documentation at initialization
        self.documentation_url = get_terraform_documentation_url(self.namespace, self.provider, 'data_source', self.data_source_type)
        self.documentation_text = get_terraform_documentation(self.namespace, self.provider, 'data_source', self.data_source_type)

    def write_data_source_code(self, data_source_name, schema):
        header = f'data "{self.provider}_{self.data_source_type}" "{data_source_name}" {{\n'
        footer = "}\n"
        self.write_line(header)
        self.write_code(schema)
        self.write_line(footer)

    def generate(self, data_source_name, schema):
        self.write_data_source_code(data_source_name, schema)
        print(self.content)
        

# data_source_generator = DataSourceGenerator("azurerm", "subnet")
# schema = get_schema()
# data_source_schema = get_data_source_schema(schema, "hashicorp", "azurerm", "subnet")
# data_source_generator.generate("my_subnet", data_source_schema)





# class VariableGenerator(BlockGenerator):
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

#     def generate(self):
#         content = ""
#         # Iterate over all .tf files in the current directory
#         for file_name in os.listdir(os.getcwd()):
#             if file_name.endswith('.tf'):
#                 with open(file_name, 'r') as tf_file:
#                     content += tf_file.read()

#         # Search attributes in the aggregated content
#         self.search_attributes(content)

#         return self.variables

# variable_generator = VariableGenerator(namespace="hashicorp", provider="azurerm", object_type="key_vault", variable_names=["test_name"])
# variables = variable_generator.generate()
# print(variables)
