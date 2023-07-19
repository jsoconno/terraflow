"""
Constant values used across the CLI.
"""
from enum import Enum
import os
import click

from terraflow.libraries.helpers import read_yaml_file, get_terraform_providers, get_namespaces_and_providers

import os

def get_config_file_path():
    if os.getcwd().endswith('terraform'):
        return '.terraflow.yaml'
    else:
        return 'terraform/.terraflow.yaml'

def namespace_option_default():
    config = read_yaml_file(filename=get_config_file_path())
    namespaces, providers = get_namespaces_and_providers()

    if namespaces:
        if config and 'namespace' in config and config['namespace'] in namespaces:
            return config['namespace']
        elif len(namespaces) == 1:
            return namespaces[0]
    else:
        return None

def provider_option_default():
    config = read_yaml_file(filename=get_config_file_path())
    namespaces, providers = get_namespaces_and_providers()

    if providers:
        if config and 'provider' in config and config['provider'] in providers:
            return config['provider']
        elif len(providers) == 1:
            return providers[0]
    else:
        return None


namespace_default = namespace_option_default()
provider_default = provider_option_default()

# Dictionary of different CLI options
options = {
    "refresh": click.option(
        "--refresh",
        type=str,
        default=False,
        is_flag=True,
        multiple=False,
        required=False,
        help="Refresh the downloaded schema file.",
    ),
    "namespace": click.option(
        "--namespace",
        type=str,
        default=namespace_default if namespace_default else 'hashicorp',
        multiple=False,
        required=False if namespace_default else True,
        help="The namespace of the Terraform provider.",
    ),
    "provider": click.option(
        "--provider",
        type=str,
        default=provider_default,
        multiple=False,
        required=False if provider_default else True,
        help="The name of the Terraform provider.",
    ),
    "kind": click.option(
        "--kind",
        type=str,
        default=None,
        multiple=False,
        required=True,
        help="The name of the terraform provider resource.",
    ),
    "name": click.option(
        "--name",
        type=str,
        default="main",
        multiple=False,
        required=False,
        help="The name to give the Terraform resource in the configuration.  For example, 'main' or 'this'.",
    ),
    "required_attributes_only": click.option(
        "--required-attributes-only",
        type=bool,
        is_flag=True,
        default=False,
        multiple=False,
        required=False,
        help="Only include required attributes in the resource configuration.",
    ),
    "required_blocks_only": click.option(
        "--required-blocks-only",
        type=bool,
        is_flag=True,
        default=False,
        multiple=False,
        required=False,
        help="Only include required blocks in the resource configuration.",
    ),
    "add_inline_descriptions": click.option(
        "--add-inline-descriptions",
        type=bool,
        is_flag=True,
        default=False,
        multiple=False,
        required=False,
        help="Add descriptions inline with the code for all resource attributes.",
    ),
    # "sync_variables": click.option(
    #     "--sync-variables",
    #     type=bool,
    #     is_flag=True,
    #     default=False,
    #     multiple=False,
    #     required=False,
    #     help="Automatically sync variables for the created resource.",
    # ),
    "add_terraform_docs_url": click.option(
        "--add-terraform-docs-url",
        type=bool,
        is_flag=True,
        default=False,
        multiple=False,
        required=False,
        help="Add a link to the documentation above the resource.",
    ),
    "exclude_block": click.option(
        "--exclude-block",
        type=str,
        default=None,
        multiple=True,
        required=False,
        help="Blocks to exclude in the configuration.",
    ),
    "exclude_attribute": click.option(
        "--exclude-attribute",
        type=str,
        default=None,
        multiple=True,
        required=False,
        help="Attributes to exclude in the configuration.",
    ),
    "header_comment": click.option(
        "--header-comment",
        type=str,
        default=None,
        multiple=False,
        required=False,
        help="A comment to add to the header of the resource.",
    ),
    # "dynamic_block": click.option(
    #     "--dynamic-block",
    #     type=str,
    #     default=None,
    #     multiple=True,
    #     required=False,
    #     help="Blocks to make dynamic in the configuration.",
    # ),
    "attribute_default": click.option(
        "--attribute-default",
        type=str,
        default=None,
        multiple=True,
        required=False,
        help="Default values for a given attributes in the format 'attribute=value'.",
    ),
    "attribute_value_prefix": click.option(
        "--attribute-value-prefix",
        type=str,
        default=None,
        multiple=False,
        required=False,
        help="A prefix to give to all variables in the resource configuration.  Useful for module development.",
    ),
    "terraform_filename": click.option(
        "--terraform-filename",
        type=str,
        default=None,
        multiple=False,
        required=False,
        help="The name of file to store Terraform resources in.",
    ),
    "variables_filename": click.option(
        "--variables-filename",
        type=str,
        default="variables.tf",
        multiple=False,
        required=False,
        help="The name of the file to store variables in.",
    ),
    "keyword": click.option(
        "--keyword",
        type=str,
        default=None,
        multiple=True,
        required=False,
        help="A keyword used to filter results.",
    ),
    "include_variable": click.option(
        "--include-variable",
        type=str,
        default=None,
        multiple=True,
        required=False,
        help="A variable to target for updates.  If not provided, all variables are updated.",
    ),
}


# Options decorators
def provider_options(func):
    """
    Description
    """
    func = options["namespace"](func)
    func = options["provider"](func)

    return func


def resource_options(func):
    """
    Description
    """
    func = options["kind"](func)
    func = options["name"](func)

    return func


def code_options(func):
    """
    Description
    """
    func = options["required_attributes_only"](func)
    func = options["required_blocks_only"](func)
    func = options["add_inline_descriptions"](func)
    # func = options["sync_variables"](func)
    # func = options["include_variable"](func)
    func = options["add_terraform_docs_url"](func)
    func = options["exclude_block"](func)
    # func = options["dynamic_block"](func)
    func = options["exclude_attribute"](func)
    func = options["attribute_default"](func)
    func = options["attribute_value_prefix"](func)
    func = options["terraform_filename"](func)
    # func = options["variables_filename"](func)
    func = options["header_comment"](func)

    return func


def schema_options(func):
    """
    Description
    """
    func = options["refresh"](func)

    return func


def terraform_file_options(func):
    """
    Description
    """
    func = options["terraform_filename"](func)

    return func


def filter_options(func):
    """
    Description
    """
    func = options["keyword"](func)

    return func

def variable_options(func):
    """
    Description
    """
    func = options["variables_filename"](func)

    return func