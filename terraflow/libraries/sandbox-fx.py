from terraflow.libraries.schema import *
from terraflow.libraries.helpers import *

def recurse_schema(schema, content, variables, outputs, attribute_func, block_func, resource_func, output_func, **kwargs):
    # Get the attributes and blocks from the schema
    attributes = schema.get("block", {}).get("attributes", {})
    blocks = schema.get("block", {}).get("block_types", {})

    # Process attributes
    for attribute, attribute_schema in attributes.items():
        content = attribute_func(content, variables, outputs, attribute_schema, **kwargs)

        # Write outputs
        output = output_func(attribute, **kwargs)
        if output:
            outputs.append(output)

    # Process blocks
    for block, block_schema in blocks.items():
        content = block_func(content, block_schema, **kwargs)
        content, variables, outputs = recurse_schema(block_schema, content, variables, outputs, attribute_func, block_func, resource_func, output_func, **kwargs)

    # Process resource
    content = resource_func(content, **kwargs)

    return content, variables, outputs


def create_providers(provider, namespace="hashicorp", schema=None, refresh=False):
    header = f'provider "{provider}" {{'
    regex_pattern = rf'(?:#.*\n)*?^provider\s+"{provider}"\s+{{[\s\S]*?^}}$'

    if refresh:
        download_schema(filename=schema, refresh=refresh)

    schema = get_schema()
    provider_schema = get_provider_schema(schema=schema, namespace=namespace, provider=provider)

    code, variables, outputs = recurse_schema(provider_schema, header, [], [], write_body_code, add_block_wrapper, add_resource_wrapper, write_output_code, **kwargs)

    # Write file
    write_to_file(text=code, filename="providers.tf", regex_pattern=regex_pattern)

    # Format code
    subprocess.run(["terraform", "fmt"], stdout=subprocess.DEVNULL)

    return code


def delete_providers(provider):
    regex_pattern = rf'^provider\s+"{provider}"\s+{{[\s\S]*?^}}\n*'

    with open("providers.tf", "r") as f:
        string = f.read()

    result = re.sub(pattern=regex_pattern, repl="", string=string, flags=re.MULTILINE)

    with open("providers.tf", "w") as f:
        f.write(result)


def create_resources(provider, resource, namespace="hashicorp", schema=None, refresh=False):
    resource = "_".join([provider, resource]) if not provider in resource else resource
    header = f'resource "{resource}" "{name}" {{'
    regex_pattern = rf'(?:#.*\n)*?^resource\s+"{resource}"\s+"{name}"\s+{{[\s\S]*?^}}$'

    if refresh:
        download_schema(filename=schema, refresh=refresh)

    schema = get_resource_schema(namespace=namespace, provider=provider, resource=resource, filename=schema)

    code, variables, outputs = recurse_schema(schema, header, [], [], write_body_code, add_block_wrapper, add_resource_wrapper, write_output_code, **kwargs)

    # Write file
    write_to_file(text=code, filename="main.tf", regex_pattern=regex_pattern)

    # Format code
    subprocess.run(["terraform", "fmt"], stdout=subprocess.DEVNULL)

    return code


def delete_resources(provider, resource, name):
    resource = "_".join([provider, resource]) if not provider in resource else resource
    regex_pattern = rf'(?:#.*\n)*?^resource\s+"{resource}"\s+"{name}"\s+{{[\s\S]*?^}}\n*'

    with open("main.tf", "r") as f:
        string = f.read()

    result = re.sub(pattern=regex_pattern, repl="", string=string, flags=re.MULTILINE)

    with open("main.tf", "w") as f:
        f.write(result)


def create_data_sources(provider, data_source, name='main', namespace="hashicorp", schema=None, refresh=False):
    data_source = "_".join([provider, data_source]) if not provider in data_source else data_source
    header = f'data "{data_source}" "{name}" {{'
    regex_pattern = rf'(?:#.*\n)*?^data\s+"{data_source}"\s+"{name}"\s+{{[\s\S]*?^}}$'

    if refresh:
        download_schema(filename=schema, refresh=refresh)
    
    schema = get_data_source_schema(namespace=namespace, provider=provider, data_source=data_source, filename=schema)

    code, variables, outputs = recurse_schema(schema, header, [], [], write_body_code, add_block_wrapper, add_resource_wrapper, write_output_code, **kwargs)

    # Write file
    write_to_file(text=code, filename="data-sources.tf", regex_pattern=regex_pattern)

    # Format code
    subprocess.run(["terraform", "fmt"], stdout=subprocess.DEVNULL)

    return code


def delete_data_sources(provider, data_source, name):
    data_source = "_".join([provider, data_source]) if not provider in data_source else data_source
    regex_pattern = rf'(?:#.*\n)*?^data\s+"{data_source}"\s+"{name}"\s+{{[\s\S]*?^}}\n*'

    with open("data-sources.tf", "r") as f:
        string = f.read()

    result = re.sub(pattern=regex_pattern, repl="", string=string, flags=re.MULTILINE)

    with open("data-sources.tf", "w") as f:
        f.write(result)

namespace = 'hashicorp'
provider = 'azurerm'
data_source = 'key_vault'

schema = get_schema()
get_data_source_schema(schema, namespace, provider, data_source)
create_data_sources(provider, data_source, namespace, schema)