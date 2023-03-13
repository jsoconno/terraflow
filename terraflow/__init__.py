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
@scope_options
@download_options
def schema_download(namespace, provider, scope, resource, attribute, blocks, filename):
    schema = get_schema(
        scope=scope,
        namespace=namespace,
        provider=provider,
        resource=resource,
        attribute=attribute,
        blocks=blocks,
        filename=filename
    )

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

# terraflow resource create
@resource.command('create', context_settings=CONTEXT_SETTINGS)
@schema_options
@scope_options
@code_options
def resource_create(
    schema,
    scope,
    namespace,
    provider,
    resource,
    resource_name,
    required_attributes_only,
    required_blocks_only,
    add_descriptions,
    ignore_block,
    ignore_attribute,
    attribute_default,
    attribute_value_prefix,
    configuration_file,
    output_code,
    overwrite_code,
    format_code,
):
    '''
    Docs
    '''
    attribute_defaults = convert_strings_to_dict(attribute_default)
    
    schema = get_schema(
        scope=scope,
        namespace=namespace,
        provider=provider,
        resource=resource,
        filename=schema
    )
    write_code(
        schema=schema,
        scope=scope,
        namespace=namespace,
        provider=provider,
        resource=resource,
        resource_name=resource_name,
        required_attributes_only=required_attributes_only,
        required_blocks_only=required_blocks_only,
        add_descriptions=add_descriptions,
        ignore_blocks=ignore_block,
        ignore_attributes=ignore_attribute,
        attribute_defaults=attribute_defaults,
        attribute_value_prefix=attribute_value_prefix,
        configuration_file=configuration_file,
        output_code=output_code,
        overwrite_code=overwrite_code,
        format_code=format_code,
    )

# terraflow variable create --namespace --provider --provider-version --name
# terraflow provider create --namespace --provider --provider-version
# terraflow documentation create --namespace --provider --provider-version 