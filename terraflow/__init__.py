import click

from terraflow.libraries.core import *
from terraflow.libraries.constants import *

CONTEXT_SETTINGS = dict(auto_envvar_prefix='terraflow')

@click.group('terraflow', invoke_without_command=True)
@click.version_option()
def terraflow():
    '''
    \b
    Terraform is an open-source infrastructure as code tool that 
    allows developers to manage cloud resources through code. 
    Terraflow provides developers with a set of commands and features 
    that can help them create, test, and deploy Terraform code more efficiently.
    
    With Terraflow, developers can easily create Terraform modules, templates, 
    and configurations using a simple and intuitive command line interface. 
    They can also quickly generate code snippets and boilerplate code, reducing 
    the amount of manual work required to create new Terraform resources.
    '''
    pass

# terraflow boot
@terraflow.group('boot')
def boot():
    '''
    Docs
    '''
    pass
# terraflow workspace
@terraflow.group('workspace')
def workspace():
    '''
    Docs
    '''
    pass
# terraflow workspace set
@workspace.command('set', context_settings=CONTEXT_SETTINGS)
def workspace_set(workspace):
    '''
    Set a workspace.
    '''
    pass
# terraflow workspace get
@workspace.command('get', context_settings=CONTEXT_SETTINGS)
def workspace_get(workspace):
    '''
    Get a workspace.
    '''
    pass
# terraflow workspace list
@workspace.command('list', context_settings=CONTEXT_SETTINGS)
def workspace_list():
    '''
    Get workspaces.
    '''
    pass
# terraflow workspace create
@workspace.command('create', context_settings=CONTEXT_SETTINGS)
def workspace_create(workspace):
    '''
    Create a workspace.
    '''
    pass
# terraflow workspace delete
@workspace.command('delete', context_settings=CONTEXT_SETTINGS)
def workspace_delete(workspace):
    '''
    Delete a workspace.
    '''
    pass

# terraflow schema
@terraflow.group('schema')
def schema():
    '''
    Schema management.
    '''
    pass

# terraflow schema download
@schema.command('download', context_settings=CONTEXT_SETTINGS)
@download_options
def schema_download(filename):
    schema = get_schema()

    download_schema(
        schema=schema,
        filename=filename
    )

# terraflow resource
@terraflow.group('resource')
def resource():
    '''
    Docs
    '''
    pass

# terraflow resource list
@resource.command('list', context_settings=CONTEXT_SETTINGS)
@provider_options
@filter_options
def resource_list(namespace, provider, keyword):
    schema = get_schema()

    items = list_items(
        schema=schema,
        namespace=namespace,
        provider=provider,
        scope='resource',
        keywords=keyword
    )

    print(pretty_list(
        title=f'Resources for {namespace} {provider}:',
        items=items
    ))

# terraflow resource create
@resource.command('create', context_settings=CONTEXT_SETTINGS)
@schema_options
@provider_options
@resource_options
@code_options
def resource_create(
    namespace,
    provider,
    resource,
    schema,
    name,
    required_attributes_only,
    required_blocks_only,
    add_descriptions,
    ignore_block,
    dynamic_block,
    ignore_attribute,
    attribute_default,
    attribute_value_prefix,
    filename
):
    '''
    Docs
    '''
    attribute_defaults = convert_strings_to_dict(attribute_default)

    write_resource_code(
        namespace=namespace,
        provider=provider,
        resource=resource,
        ignore_attributes=ignore_attribute,
        ignore_blocks=ignore_block,
        dynamic_blocks=dynamic_block,
        required_attributes_only=required_attributes_only,
        required_blocks_only=required_blocks_only,
        add_descriptions=add_descriptions,
        attribute_defaults=attribute_defaults,
        attribute_value_prefix=attribute_value_prefix,
        filename=filename,
        name=name,
        schema=schema
    )

# terraflow data-source
@terraflow.group('data-source')
def data_source():
    '''
    Docs
    '''
    pass

# terraflow data source list
@data_source.command('list', context_settings=CONTEXT_SETTINGS)
@provider_options
@filter_options
def data_source_list(namespace, provider, keyword):
    schema = get_schema()

    items = list_items(
        schema=schema,
        namespace=namespace,
        provider=provider,
        scope='data_source',
        keywords=keyword
    )

    print(pretty_list(
        title=f'Data sources for {namespace} {provider}:',
        items=items
    ))

# terraflow data-source create
@data_source.command('create', context_settings=CONTEXT_SETTINGS)
@schema_options
@provider_options
@resource_options
@code_options
def data_source_create(
    namespace,
    provider,
    resource,
    schema,
    name,
    required_attributes_only,
    required_blocks_only,
    add_descriptions,
    ignore_block,
    dynamic_block,
    ignore_attribute,
    attribute_default,
    attribute_value_prefix,
    filename
):
    '''
    Docs
    '''
    attribute_defaults = convert_strings_to_dict(attribute_default)

    write_data_source_code(
        namespace=namespace,
        provider=provider,
        resource=resource,
        ignore_attributes=ignore_attribute,
        ignore_blocks=ignore_block,
        dynamic_blocks=dynamic_block,
        required_attributes_only=required_attributes_only,
        required_blocks_only=required_blocks_only,
        add_descriptions=add_descriptions,
        attribute_defaults=attribute_defaults,
        attribute_value_prefix=attribute_value_prefix,
        filename=filename,
        name=name,
        schema=schema
    )

# terraflow variable create --namespace --provider --provider-version --name

# terraflow provider
@terraflow.group('provider')
def provider():
    '''
    Docs
    '''
    pass

# terraflow provider list
@provider.command('list', context_settings=CONTEXT_SETTINGS)
@filter_options
def provider_list(keyword):
    schema = get_schema()

    items = list_items(
        schema=schema,
        scope='provider',
        keywords=keyword
    )

    print(pretty_list(
        title='Providers in this configuration:',
        items=items
    ))

# terraflow provider create
@provider.command('create', context_settings=CONTEXT_SETTINGS)
@schema_options
@provider_options
@code_options
def provider_create(
    namespace,
    provider,
    schema,
    required_attributes_only,
    required_blocks_only,
    add_descriptions,
    ignore_block,
    dynamic_block,
    ignore_attribute,
    attribute_default,
    attribute_value_prefix,
    filename
):
    '''
    Docs
    '''
    attribute_defaults = convert_strings_to_dict(attribute_default)
    
    write_provider_code(
        namespace=namespace,
        provider=provider,
        ignore_attributes=ignore_attribute,
        ignore_blocks=ignore_block,
        dynamic_blocks=dynamic_block,
        required_attributes_only=required_attributes_only,
        required_blocks_only=required_blocks_only,
        add_descriptions=add_descriptions,
        attribute_defaults=attribute_defaults,
        attribute_value_prefix=attribute_value_prefix,
        filename=filename,
        schema=schema
    )

# terraflow documentation create --namespace --provider --provider-version 