"""
Constant values used across the CLI.
"""
from enum import Enum
import os
import click

# Validation
ALLOWED_SCOPES = ["provider", "resource", "data_source"]
ALLOWED_ATTRIBUTES = ["optional", "required", "description", "type"]

# Dictionary of different CLI options
options = {
    "schema_filename": click.option(
        "--schema-filename",
        type=str,
        default="schema.json",
        multiple=False,
        required=False,
        help="The name of the Terraform schema to use locally.",
    ),
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
        default="hashicorp",
        multiple=False,
        required=True,
        help="The namespace of the Terraform provider.",
    ),
    "provider": click.option(
        "--provider",
        type=str,
        default=None,
        multiple=False,
        required=True,
        help="The name of the Terraform provider.",
    ),
    "resource": click.option(
        "--resource",
        type=str,
        default=None,
        multiple=False,
        required=True,
        help="The name of the terraform provider resource.",
    ),
    "name": click.option(
        "--name", type=str, default="main", multiple=False, required=False, help="The name to give the Terraform resource in the configuration.  For example, 'main' or 'this'."
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
    "add_descriptions": click.option(
        "--add-descriptions",
        type=bool,
        is_flag=True,
        default=False,
        multiple=False,
        required=False,
        help="Add descriptions inline with the code for all resource attributes.",
    ),
    "ignore_block": click.option(
        "--ignore-block", type=str, default=None, multiple=True, required=False, help="Blocks to ignore in the configuration."
    ),
    "ignore_attribute": click.option(
        "--ignore-attribute",
        type=str,
        default=None,
        multiple=True,
        required=False,
        help="Attributes to ignore in the configuration."
    ),
    "dynamic_block": click.option(
        "--dynamic-block",
        type=str,
        default=None,
        multiple=True,
        required=False,
        help="Blocks to make dynamic in the configuration."
    ),
    "attribute_default": click.option(
        "--attribute-default",
        type=str,
        default=None,
        multiple=True,
        required=False,
        help="Default values for a given attributes in the format 'attribute=value'."
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
        default="main.tf",
        multiple=False,
        required=False,
        help="The name of the target Terraform file.",
    ),
    "keyword": click.option(
        "--keyword", type=str, default=None, multiple=True, required=False, help="A keyword used to filter results."
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
    func = options["resource"](func)
    func = options["name"](func)

    return func


def code_options(func):
    """
    Description
    """
    func = options["required_attributes_only"](func)
    func = options["required_blocks_only"](func)
    func = options["add_descriptions"](func)
    func = options["ignore_block"](func)
    func = options["dynamic_block"](func)
    func = options["ignore_attribute"](func)
    func = options["attribute_default"](func)
    func = options["attribute_value_prefix"](func)
    func = options["terraform_filename"](func)

    return func


def schema_file_options(func):
    """
    Description
    """
    func = options["schema_filename"](func)
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
