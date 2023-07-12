#!/usr/bin/env python3

import click
from dataclasses import asdict

from terraflow.libraries.helpers import *
from terraflow.libraries.constants import *
from terraflow.libraries.schema import *
from terraflow.libraries.terraform import *
from terraflow.libraries.configuration import *
from terraflow.libraries.options import *
from terraflow.version import __version__

CONTEXT_SETTINGS = dict(auto_envvar_prefix="terraflow")


@click.group("terraflow", invoke_without_command=True)
@click.version_option(version=__version__, prog_name="terraflow")
def terraflow():
    """
    \b
    Terraform is an open-source infrastructure as code tool that
    allows developers to manage cloud resources through code.
    Terraflow provides developers with a set of commands and features
    that can help them create, test, and deploy Terraform code more efficiently.

    With Terraflow, developers can easily create Terraform modules, templates,
    and configurations using a simple and intuitive command line interface.
    They can also quickly generate code snippets and boilerplate code, reducing
    the amount of manual work required to create new Terraform resources.
    """
    pass

# terraflow schema
@terraflow.group("schema")
def schema():
    """
    Manage the schema file.
    """
    pass

# terraflow schema refresh
@schema.command("refresh", context_settings=CONTEXT_SETTINGS)
def schema_refresh():
    """
    Refresh the schema file.
    """
    schema = get_schema(refresh=True)

# terraflow provider
@terraflow.group("provider")
def provider():
    """
    Manage Terraform providers.
    """
    pass


# terraflow provider list
@provider.command("list", context_settings=CONTEXT_SETTINGS)
@provider_options
def provider_list(namespace, provider):
    """
    List available providers.
    """
    items = get_terraform_providers(
        namespace=namespace
    )

    print(format_list(title=f"Available providers for namespace {namespace}:", items=items))


# terraflow provider get
@provider.command("get", context_settings=CONTEXT_SETTINGS)
@filter_options
def provider_get(keyword):
    """
    Get providers in the Terraform configuration.
    """
    schema = get_schema()

    items = list_items(schema=schema, scope="provider", keywords=keyword)

    print(format_list(title="Providers in this configuration:", items=items))


# terraflow resource
@terraflow.group("resource")
def resource():
    """
    Manage Terraform resources.
    """
    pass


# terraflow resource list
@resource.command("list", context_settings=CONTEXT_SETTINGS)
@provider_options
@filter_options
def resource_list(namespace, provider, keyword):
    """
    List available resources for a provider.
    """
    schema = get_schema()

    items = list_items(
        schema=schema,
        namespace=namespace,
        provider=provider,
        scope="resource",
        keywords=keyword,
    )

    print(format_list(items=items, title=f"Resources for {namespace} {provider}:"))


# terraflow resource create
@resource.command("create", context_settings=CONTEXT_SETTINGS)
@schema_options
@terraform_file_options
@provider_options
@resource_options
@code_options
def resource_create(
    namespace,
    provider,
    kind,
    refresh,
    name,
    required_attributes_only,
    required_blocks_only,
    add_inline_descriptions,
    # sync_variables,
    add_terraform_docs_url,
    exclude_block,
    # dynamic_block,
    exclude_attribute,
    attribute_default,
    attribute_value_prefix,
    terraform_filename,
    header_comment,
    # include_variable,
    # variables_filename
):
    """
    Create a Terraform resource.
    """
    attribute_defaults = convert_strings_to_dict(attribute_default)

    configuration = ResourceConfiguration(
        add_inline_descriptions=add_inline_descriptions,
        add_header_terraform_docs_url=add_terraform_docs_url,
        required_attributes_only=required_attributes_only,
        required_blocks_only=required_blocks_only,
        exclude_attributes=exclude_attribute,
        exclude_blocks=exclude_block,
        attribute_defaults=attribute_defaults,
        header_comment=header_comment,
        attribute_value_prefix=attribute_value_prefix,
    )

    resource = ResourceComponent(
        namespace=namespace,
        provider=provider,
        kind=kind,
        name=name,
        configuration=configuration
    )

    write_terraform_to_file(
        new_code=resource.code,
        filename=terraform_filename
    )
    
    # TODO: This is not always adding a new resource so the message or logic should be adjusted.
    print(f'\n{colors(color="OK_GREEN")}Success:{colors()} The resource "{provider}_{kind}" "{name}" was added to the Terraform configuration.\n')

    # Remove hard coding and add flag later

    # if sync_variables:
    #     variable_config = ResourceConfiguration(
    #         add_descriptions=True
    #     )

    #     variables_code = this.get_variables(config=asdict(variable_config))

    #     write_terraform_to_file(
    #         new_code=variables_code,
    #         filename=variables_filename
    #     )

    #     remove_unused_variables()

    run_terraform_fmt()

# terraflow resource update
@resource.command("update", context_settings=CONTEXT_SETTINGS)
@provider_options
@resource_options
def resource_create(
    namespace,
    provider,
    kind,
    name,
    #rename,
    #set_attribute,
    #make_block_dynamic,

):
    """
    Update a Terraform resource.
    """

    loader = CodeLoader()
    code = loader.get_component_code_by_id(
        id=f"resource.{provider}_{resource}.{name}"
    )
    print(code)

# terraflow resource delete
@resource.command("delete", context_settings=CONTEXT_SETTINGS)
@provider_options
@resource_options
def resource_delete(namespace, provider, kind, name):
    """
    Delete a resource from the configuration.
    """
    loader = CodeLoader()
    component = loader.get_component_by_id(
        id=f"resource.{provider}_{kind}.{name}"
    )

    if component:
        delete_resource_code(
            provider=provider, kind=component["kind"], name=component["name"], filename=component["filename"]
        )
        print(f'\n{colors(color="OK_GREEN")}Success:{colors()} The resource "{provider}_{kind}" "{name}" was deleted from the Terraform configuration.\n')
    else:
        print(f'\n{colors(color="FAIL")}Error:{colors()} The resource "{provider}_{kind}" "{name}" does not exist in the Terraform configuration.\n')

    remove_unused_variables()

# terraflow data
@terraflow.group("data")
def data():
    """
    Manage Terraform data sources.
    """
    pass


# terraflow data source list
@data.command("list", context_settings=CONTEXT_SETTINGS)
@provider_options
@filter_options
def data_list(namespace, provider, keyword):
    """
    List available data sources for a provider.
    """
    schema = get_schema()

    items = list_items(
        schema=schema,
        namespace=namespace,
        provider=provider,
        scope="data_source",
        keywords=keyword,
    )

    print(format_list(items=items, title=f"Data sources for {namespace} {provider}:"))


# terraflow variable
@terraflow.group("variable")
def variable():
    """
    Manage Terraform variables.
    """
    pass
