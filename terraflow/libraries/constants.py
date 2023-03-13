'''
Constant values used across the CLI.
'''
from enum import Enum
import click

# Validation
ALLOWED_SCOPES = ["provider", "resource", "data_source"]
ALLOWED_ATTRIBUTES = ["optional", "required", "description", "type"]

# Help text
SCHEMA = 'The name of the schema to use for resource creation.'
NAMESPACE = 'The namespace for the Terraform provider.'
PROVIDER = 'The name of the Terraform provider.'
RESOURCE = 'The target Terraform resource name.'
ATTRIBUTE = 'The name of the Terraform resource attribute.'
BLOCKS = 'A list of the blocks where the attribute can be found.'
FILENAME = 'The name of the file.'

# Dictionary of different CLI options
options = {
    'schema': click.option(
        '--schema',
        type=str,
        default=None,
        multiple=False,
        required=False,
        help=SCHEMA
    ),
    'namespace': click.option(
        '--namespace',
        type=str,
        default='hashicorp',
        multiple=False,
        required=False,
        help=NAMESPACE
    ),
    'provider': click.option(
        '--provider',
        type=str,
        default=None,
        multiple=False,
        required=False,
        help=PROVIDER
    ),
    'resource': click.option(
        '--resource',
        type=str,
        default=None,
        multiple=False,
        required=False,
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
    'filename': click.option(
        '--filename',
        type=str,
        default=None,
        multiple=False,
        required=False,
        help=FILENAME
    ),
    'resource_name': click.option(
        '--resource-name',
        type=str,
        default='main',
        multiple=False,
        required=False,
        help=''
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
    'configuration_file': click.option(
        '--configuration-file',
        type=str,
        default='main.tf',
        multiple=False,
        required=False,
        help=''
    ),
    'output_code': click.option(
        '--output-code',
        type=bool,
        is_flag=True,
        default=True,
        multiple=False,
        required=False,
        help=''
    ),
    'overwrite_code': click.option(
        '--overwrite-code',
        type=bool,
        is_flag=True,
        default=True,
        multiple=False,
        required=False,
        help=''
    ),
    'format_code': click.option(
        '--format-code',
        type=bool,
        is_flag=True,
        default=True,
        multiple=False,
        required=False,
        help=''
    ),
}
# Options decorators
def schema_options(func):
    '''
    Description
    '''
    func = options['schema'](func)

    return func

def scope_options(func):
    '''
    Description
    '''
    func = options['namespace'](func)
    func = options['provider'](func)
    func = options['resource'](func)

    return func

def download_options(func):
    '''
    Description
    '''
    func = options['attribute'](func)
    func = options['blocks'](func)
    func = options['filename'](func)

    return func

def code_options(func):
    '''
    Description
    '''
    func = options['resource_name'](func)
    func = options['required_attributes_only'](func)
    func = options['required_blocks_only'](func)
    func = options['add_descriptions'](func)
    func = options['ignore_block'](func)
    func = options['ignore_attribute'](func)
    func = options['attribute_default'](func)
    func = options['attribute_value_prefix'](func)
    func = options['configuration_file'](func)
    func = options['output_code'](func)
    func = options['overwrite_code'](func)
    func = options['format_code'](func)

    return func