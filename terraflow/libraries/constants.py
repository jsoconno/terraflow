'''
Constant values used across the CLI.
'''
from enum import Enum
import os
import click

# Validation
ALLOWED_SCOPES = ['provider', 'resource', 'data_source']
ALLOWED_ATTRIBUTES = ['optional', 'required', 'description', 'type']

# Help text
SCHEMA = 'The name of the schema to use for resource creation.'
NAMESPACE = 'The namespace for the Terraform provider.'
PROVIDER = 'The name of the Terraform provider.'
NAME = 'The name of the resource or data source.'
RESOURCE = 'The target Terraform resource name.'
ATTRIBUTE = 'The name of the Terraform resource attribute.'
BLOCKS = 'A list of the blocks where the attribute can be found.'
FILENAME = 'The name of the Terraform configuration file.'
KEYWORD = 'Keyword used to filter the list.'

# Dictionary of different CLI options
options = {
    'schema': click.option(
        '--schema',
        type=str,
        default='schema.json' if os.path.isfile('schema.json') else None,
        multiple=False,
        required=False,
        help=SCHEMA
    ),
    'namespace': click.option(
        '--namespace',
        type=str,
        default='hashicorp',
        multiple=False,
        required=True,
        help=NAMESPACE
    ),
    'provider': click.option(
        '--provider',
        type=str,
        default=None,
        multiple=False,
        required=True,
        help=PROVIDER
    ),
    'resource': click.option(
        '--resource',
        type=str,
        default=None,
        multiple=False,
        required=True,
        help=RESOURCE
    ),
    'attribute': click.option(
        '--attribute',
        type=str,
        default=None,
        multiple=False,
        required=False,
        help=ATTRIBUTE
    ),
    'blocks': click.option(
        '--blocks',
        type=list,
        default=None,
        multiple=False,
        required=False,
        help=BLOCKS
    ),
    'name': click.option(
        '--name',
        type=str,
        default='main',
        multiple=False,
        required=False,
        help=NAME
    ),
    'required_attributes_only': click.option(
        '--required-attributes-only',
        type=bool,
        is_flag=True,
        default=False,
        multiple=False,
        required=False,
        help=''
    ),
    'required_blocks_only': click.option(
        '--required-blocks-only',
        type=bool,
        is_flag=True,
        default=False,
        multiple=False,
        required=False,
        help=''
    ),
    'add_descriptions': click.option(
        '--add-descriptions',
        type=bool,
        is_flag=True,
        default=False,
        multiple=False,
        required=False,
        help=''
    ),
    'ignore_block': click.option(
        '--ignore-block',
        type=str,
        default=None,
        multiple=True,
        required=False,
        help=''
    ),
    'ignore_attribute': click.option(
        '--ignore-attribute',
        type=str,
        default=None,
        multiple=True,
        required=False,
        help=''
    ),
    'dynamic_block': click.option(
        '--dynamic-block',
        type=str,
        default=None,
        multiple=True,
        required=False,
        help=''
    ),
    'attribute_default': click.option(
        '--attribute-default',
        type=str,
        default=None,
        multiple=True,
        required=False,
        help=''
    ),
    'attribute_value_prefix': click.option(
        '--attribute-value-prefix',
        type=str,
        default=None,
        multiple=False,
        required=False,
        help=''
    ),
    'filename': click.option(
        '--filename',
        type=str,
        default='main.tf',
        multiple=False,
        required=False,
        help=''
    ),
    'keyword': click.option(
        '--keyword',
        type=str,
        default=None,
        multiple=True,
        required=False,
        help=KEYWORD
    ),
}
# Options decorators
def schema_options(func):
    '''
    Description
    '''
    func = options['schema'](func)

    return func

def provider_options(func):
    '''
    Description
    '''
    func = options['namespace'](func)
    func = options['provider'](func)

    return func

def resource_options(func):
    '''
    Description
    '''
    func = options['resource'](func)
    func = options['name'](func)

    return func

def code_options(func):
    '''
    Description
    '''
    func = options['required_attributes_only'](func)
    func = options['required_blocks_only'](func)
    func = options['add_descriptions'](func)
    func = options['ignore_block'](func)
    func = options['dynamic_block'](func)
    func = options['ignore_attribute'](func)
    func = options['attribute_default'](func)
    func = options['attribute_value_prefix'](func)
    func = options['filename'](func)

    return func

def download_options(func):
    '''
    Description
    '''
    func = options['filename'](func)

    return func

def filter_options(func):
    '''
    Description
    '''
    func = options['keyword'](func)

    return func