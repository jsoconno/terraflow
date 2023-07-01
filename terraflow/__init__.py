#!/usr/bin/env python3

import click
from dataclasses import asdict

from terraflow.libraries.helpers import *
from terraflow.libraries.constants import *
from terraflow.libraries.schema import *
from terraflow.libraries.sandbox import *
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


# # terraflow workspace
# @terraflow.group("workspace")
# def workspace():
#     """
#     \b
#     Manage workspaces.
#     """
#     pass


# # terraflow workspace set
# @workspace.command("set", context_settings=CONTEXT_SETTINGS)
# def workspace_set(workspace):
#     """
#     Set a workspace.
#     """
#     pass


# # terraflow workspace get
# @workspace.command("get", context_settings=CONTEXT_SETTINGS)
# def workspace_get(workspace):
#     """
#     Get a workspace.
#     """
#     pass


# # terraflow workspace list
# @workspace.command("list", context_settings=CONTEXT_SETTINGS)
# def workspace_list():
#     """
#     List workspaces.
#     """
#     pass


# # terraflow workspace create
# @workspace.command("create", context_settings=CONTEXT_SETTINGS)
# def workspace_create(workspace):
#     """
#     Create a workspace.
#     """
#     pass


# # terraflow workspace delete
# @workspace.command("delete", context_settings=CONTEXT_SETTINGS)
# def workspace_delete(workspace):
#     """
#     Delete a workspace.
#     """
#     pass


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
@schema_file_options
@terraform_file_options
@provider_options
@resource_options
@code_options
def resource_create(
    namespace,
    provider,
    resource,
    refresh,
    name,
    required_attributes_only,
    required_blocks_only,
    add_descriptions,
    sync_variables,
    # add_documentation_url,
    ignore_block,
    # dynamic_block,
    ignore_attribute,
    attribute_default,
    # attribute_value_prefix,
    terraform_filename,
    include_variable,
    variables_filename
):
    """
    Create a Terraform resource.
    """
    attribute_defaults = convert_strings_to_dict(attribute_default)

    config = ResourceConfiguration(
        add_descriptions=add_descriptions,
        required_attributes_only=required_attributes_only,
        required_blocks_only=required_blocks_only,
        exclude_attributes=ignore_attribute,
        exclude_blocks=ignore_block
    )

    this = Resource(
        namespace=namespace,
        provider=provider,
        resource=resource,
        name=name
    )

    code = this.get_code(config=asdict(config))

    write_terraform_to_file(
        new_code=code,
        filename=terraform_filename
    )

    # Remove hard coding and add flag later

    if sync_variables:
        variable_config = ResourceConfiguration(
            add_descriptions=True
        )

        variables_code = this.get_variables(config=asdict(variable_config))

        write_terraform_to_file(
            new_code=variables_code,
            filename=variables_filename
        )

        remove_unused_variables()

    run_terraform_fmt()

# terraflow resource delete
@resource.command("delete", context_settings=CONTEXT_SETTINGS)
@terraform_file_options
@provider_options
@resource_options
def resource_delete(namespace, provider, resource, name, terraform_filename):
    """
    Delete a resource from the configuration.
    """
    delete_resource_code(
        provider=provider, resource=resource, name=name, filename=terraform_filename
    )


# terraflow data-source
@terraflow.group("data-source")
def data_source():
    """
    Manage Terraform data sources.
    """
    pass


# terraflow data source list
@data_source.command("list", context_settings=CONTEXT_SETTINGS)
@provider_options
@filter_options
def data_source_list(namespace, provider, keyword):
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


# # terraflow data-source create
# @data_source.command("create", context_settings=CONTEXT_SETTINGS)
# @schema_file_options
# @terraform_file_options
# @provider_options
# @resource_options
# @code_options
# def data_source_create(
#     namespace,
#     provider,
#     resource,
#     schema_filename,
#     refresh,
#     name,
#     required_attributes_only,
#     required_blocks_only,
#     add_descriptions,
#     add_documentation_url,
#     ignore_block,
#     dynamic_block,
#     ignore_attribute,
#     attribute_default,
#     attribute_value_prefix,
#     terraform_filename,
# ):
#     """
#     Create a data source.
#     """
#     attribute_defaults = convert_strings_to_dict(attribute_default)

#     create_data_source_code(
#         namespace=namespace,
#         provider=provider,
#         resource=resource,
#         ignore_attributes=ignore_attribute,
#         ignore_blocks=ignore_block,
#         dynamic_blocks=dynamic_block,
#         required_attributes_only=required_attributes_only,
#         required_blocks_only=required_blocks_only,
#         add_descriptions=add_descriptions,
#         add_documentation_url=add_documentation_url,
#         attribute_defaults=attribute_defaults,
#         attribute_value_prefix=attribute_value_prefix,
#         filename=terraform_filename,
#         name=name,
#         schema=schema_filename,
#         refresh=refresh
#     )


# # terraflow datasource delete
# @data_source.command("delete", context_settings=CONTEXT_SETTINGS)
# @terraform_file_options
# @provider_options
# @resource_options
# def data_source_delete(namespace, provider, resource, name, terraform_filename):
#     """
#     Delete a data source from the configuration.
#     """
#     delete_data_source_code(
#         provider=provider, resource=resource, name=name, filename=terraform_filename
#     )


# # terraflow variable create --namespace --provider --provider-version --name


# terraflow provider
@terraflow.group("provider")
def provider():
    """
    Manage Terraform providers.
    """
    pass


# terraflow provider get
@provider.command("get", context_settings=CONTEXT_SETTINGS)
@filter_options
def provider_list(keyword):
    """
    Get providers in the Terraform configuration.
    """
    schema = get_schema()

    items = list_items(schema=schema, scope="provider", keywords=keyword)

    print(format_list(title="Providers in this configuration:", items=items))


# # terraflow provider create
# @provider.command("create", context_settings=CONTEXT_SETTINGS)
# @schema_file_options
# @terraform_file_options
# @provider_options
# @code_options
# def provider_create(
#     namespace,
#     provider,
#     schema_filename,
#     refresh,
#     required_attributes_only,
#     required_blocks_only,
#     add_descriptions,
#     add_documentation_url,
#     ignore_block,
#     dynamic_block,
#     ignore_attribute,
#     attribute_default,
#     attribute_value_prefix,
#     terraform_filename,
# ):
#     """
#     Create a provider.
#     """
#     attribute_defaults = convert_strings_to_dict(attribute_default)

#     create_provider_code(
#         namespace=namespace,
#         provider=provider,
#         ignore_attributes=ignore_attribute,
#         ignore_blocks=ignore_block,
#         dynamic_blocks=dynamic_block,
#         required_attributes_only=required_attributes_only,
#         required_blocks_only=required_blocks_only,
#         add_descriptions=add_descriptions,
#         add_documentation_url=add_documentation_url,
#         attribute_defaults=attribute_defaults,
#         attribute_value_prefix=attribute_value_prefix,
#         filename=terraform_filename,
#         schema=schema_filename,
#         refresh=refresh
#     )


# # terraflow provider delete
# @provider.command("delete", context_settings=CONTEXT_SETTINGS)
# @terraform_file_options
# @provider_options
# def provider_delete(namespace, provider, terraform_filename):
#     """
#     Delete a provider from the configuration.
#     """
#     delete_provider_code(provider=provider, filename=terraform_filename)


# terraflow variable
@terraflow.group("variable")
def variable():
    """
    Manage Terraform variables.
    """
    pass

# terraflow variable create
@variable.command("create", context_settings=CONTEXT_SETTINGS)
@schema_file_options
@terraform_file_options
@provider_options
@resource_options
@variable_options
@code_options
def variable_create(
    namespace,
    provider,
    resource,
    refresh,
    name,
    required_attributes_only,
    required_blocks_only,
    add_descriptions,
    # add_documentation_url,
    ignore_block,
    # dynamic_block,
    ignore_attribute,
    attribute_default,
    # attribute_value_prefix,
    terraform_filename,
    include_variable
):
    """
    Create a Terraform variable(s).
    """
    attribute_defaults = convert_strings_to_dict(attribute_default)

    config = VariableConfiguration(
        add_descriptions=add_descriptions,
        include_variables=list(include_variable)
    )

    this = Resource(
        namespace=namespace,
        provider=provider,
        resource=resource,
        name=name
    )

    this.get_code()
    code = this.get_variables(config=asdict(config))

    write_terraform_to_file(
        new_code=code,
        filename='variables.tf'
    )

    run_terraform_fmt()


# # terraflow documentation
# @terraflow.group("docs")
# def docs():
#     """
#     Manage documentation.
#     """
#     pass


# # terraflow documentation create
# @docs.command("create", context_settings=CONTEXT_SETTINGS)
# @click.option(
#     "--module-path", required=True, default=".", help="Path to the Terraform module"
# )
# @click.option(
#     "--config-filename",
#     default="terraform-docs.yaml",
#     help="Filename for the terraform-docs configuration file",
# )
# def docs_create(module_path, config_filename):
#     """
#     Generate Terraform documentation using terraform-docs.

#     This command generates a markdown table of the Terraform module's
#     configuration and saves it to a README.md file in the module's
#     directory.
#     """
#     create_terraform_docs_config_file(config_filename)
#     generate_terraform_docs(module_path, config_filename)


# if __name__ == "__main__":
#     terraflow()
