#!/usr/bin/env python3

import click
from dataclasses import asdict

from .libraries.helpers import *
from .libraries.constants import *
from .libraries.schema import *
from .libraries.terraform import *
from .libraries.configuration import *
from .libraries.options import *
from .libraries.formatting import *
from .version import __version__

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
    items = get_terraform_providers(namespace=namespace)

    output = format_list(
        title=f"Available providers for namespace {namespace}:", items=items
    )
    click.echo_via_pager(output)


# terraflow provider get
@provider.command("get", context_settings=CONTEXT_SETTINGS)
@filter_options
def provider_get(keyword):
    """
    Get providers in the Terraform configuration.
    """
    schema = Schema().schema

    items = list_items(schema=schema, scope="provider", keywords=keyword)

    output = format_list(title="Providers in this configuration:", items=items)
    click.echo_via_pager(output)


# terraflow provider create
@provider.command("create", context_settings=CONTEXT_SETTINGS)
@schema_options
@terraform_file_options
@provider_options
@code_options
def resource_create(
    namespace,
    provider,
    refresh,
    required_attributes_only,
    required_blocks_only,
    add_inline_descriptions,
    add_terraform_docs_url,
    exclude_block,
    exclude_attribute,
    attribute_default,
    attribute_value_prefix,
    terraform_filename,
    header_comment,
):
    """
    Create a Terraform provider.
    """
    schema = Schema(refresh=refresh)
    attribute_defaults = convert_strings_to_dict(attribute_default)

    configuration = ProviderConfiguration(
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

    component = TerraformProvider(
        schema=schema, namespace=namespace, name=provider, configuration=configuration
    )

    write_terraform_to_file(
        new_code=component.code,
        filename=terraform_filename if terraform_filename else "providers.tf",
    )

    print(
        f'\n{colors(color="OK_GREEN")}Success:{colors()} The provider "{provider}" was created.\n'
    )

    run_terraform_fmt()


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
    schema = Schema().schema

    items = list_items(
        schema=schema,
        namespace=namespace,
        provider=provider,
        scope="resource",
        keywords=keyword,
    )

    output = format_list(items=items, title=f"Resources for {namespace} {provider}:")
    click.echo_via_pager(output)


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
    add_terraform_docs_url,
    exclude_block,
    exclude_attribute,
    attribute_default,
    attribute_value_prefix,
    terraform_filename,
    header_comment,
):
    """
    Create a Terraform resource.
    """
    schema = Schema(refresh=refresh)
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

    resource = TerraformResource(
        schema=schema,
        namespace=namespace,
        provider=provider,
        kind=kind,
        name=name,
        configuration=configuration,
    )

    write_terraform_to_file(
        new_code=resource.code,
        filename=terraform_filename if terraform_filename else "main.tf",
    )

    print(
        f'\n{colors(color="OK_GREEN")}Success:{colors()} The resource "{provider}_{kind}" "{name}" was created.\n'
    )

    run_terraform_fmt()


# terraflow resource delete
@resource.command("delete", context_settings=CONTEXT_SETTINGS)
@provider_options
@resource_options
def resource_delete(namespace, provider, kind, name):
    """
    Delete a resource from the configuration.
    """
    loader = CodeLoader()
    component = loader.get_component_by_id(id=f"resource.{provider}_{kind}.{name}")

    if component:
        delete_resource_code(
            provider=provider,
            kind=component["kind"],
            name=component["name"],
            filename=component["filename"],
        )
        print(
            f'\n{colors(color="OK_GREEN")}Success:{colors()} The resource "{provider}_{kind}" "{name}" was deleted from the Terraform configuration.\n'
        )
    else:
        print(
            f'\n{colors(color="FAIL")}Error:{colors()} The resource "{provider}_{kind}" "{name}" does not exist in the Terraform configuration.\n'
        )

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
    schema = Schema().schema

    items = list_items(
        schema=schema,
        namespace=namespace,
        provider=provider,
        scope="data_source",
        keywords=keyword,
    )

    output = format_list(items=items, title=f"Data sources for {namespace} {provider}:")
    click.echo_via_pager(output)


@data.command("create", context_settings=CONTEXT_SETTINGS)
@schema_options
@terraform_file_options
@provider_options
@resource_options
@code_options
def data_create(
    namespace,
    provider,
    kind,
    refresh,
    name,
    required_attributes_only,
    required_blocks_only,
    add_inline_descriptions,
    add_terraform_docs_url,
    exclude_block,
    exclude_attribute,
    attribute_default,
    attribute_value_prefix,
    terraform_filename,
    header_comment,
):
    """
    Create a Terraform data source.
    """
    schema = Schema(refresh=refresh)
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

    component = TerraformDataSource(
        schema=schema,
        namespace=namespace,
        provider=provider,
        kind=kind,
        name=name,
        configuration=configuration,
    )

    write_terraform_to_file(
        new_code=component.code,
        filename=terraform_filename if terraform_filename else "data.tf",
    )

    print(
        f'\n{colors(color="OK_GREEN")}Success:{colors()} The data source "{provider}_{kind}" "{name}" was created.\n'
    )

    run_terraform_fmt()


# terraflow data source delete
@data.command("delete", context_settings=CONTEXT_SETTINGS)
@provider_options
@resource_options
def resource_delete(namespace, provider, kind, name):
    """
    Delete a data source from the configuration.
    """
    loader = CodeLoader()
    component = loader.get_component_by_id(id=f"data.{provider}_{kind}.{name}")

    if component:
        delete_data_source_code(
            provider=provider,
            kind=component["kind"],
            name=component["name"],
            filename=component["filename"],
        )
        print(
            f'\n{colors(color="OK_GREEN")}Success:{colors()} The data source "{provider}_{kind}" "{name}" was deleted from the Terraform configuration.\n'
        )
    else:
        print(
            f'\n{colors(color="FAIL")}Error:{colors()} The data source "{provider}_{kind}" "{name}" does not exist in the Terraform configuration.\n'
        )

    remove_unused_variables()
    # TODO: Add remove_orphaned_outputs()


# terraflow variable
@terraflow.group("variable")
def variable():
    """
    Manage Terraform variables.
    """
    pass


# terraflow variable create
@variable.command("create", context_settings=CONTEXT_SETTINGS)
@provider_options
@resource_options
@variable_options
def variable_create(
    namespace,
    provider,
    kind,
    name,
    description,
    default,
    type,
    terraform_filename,
):
    """
    Create a Terraform variable.
    """
    schema = Schema()
    configuration = VariableConfiguration()
    component = TerraformVariable(
        schema=schema,
        name=name,
        namespace=namespace,
        provider=provider,
        kind=kind,
        type=type,
        description=description,
        variable_type="string",
        default=default,
        configuration=configuration,
    )

    write_terraform_to_file(
        new_code=component.code,
        filename=terraform_filename if terraform_filename else "variables.tf",
    )
