from core import *

scope = 'resource'
namespace = 'hashicorp'
provider= 'azurerm'
resource = 'azurerm_storage_account'


resource_schema = get_schema(
    schema_file='/Users/justinoconnor/Code/terraform-writer/terraform/full_schema.json',
    namespace=namespace,
    provider=provider,
    scope=scope,
    resource=resource,
    # blocks=['acl'],
    # attribute='access_policy'
)

code = write_code(
    schema=resource_schema,
    scope=scope,
    provider=provider,
    resource=resource,
    ignore_blocks=['timeouts'],
    attribute_value_prefix="role_assignment",
    attribute_defaults={'name': 'test'},
    resource_name='other',
    required_attributes_only=False,
    required_blocks_only=False,
    # add_descriptions=True,
    overwrite_code=True,
)