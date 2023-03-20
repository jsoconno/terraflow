/**
 * # Main title
 *
 * Everything in this comment block will get extracted into docs.
 *
 * You can put simple text or complete Markdown content
 * here. Subsequently if you want to render AsciiDoc format
 * you can put AsciiDoc compatible content in this comment
 * block.
 */

resource "azurerm_resource_group" "other" {
  location = var.location
  name     = var.name
}

resource "azurerm_key_vault" "main" {
  enable_rbac_authorization       = var.enable_rbac_authorization
  enabled_for_deployment          = var.enabled_for_deployment
  enabled_for_disk_encryption     = var.enabled_for_disk_encryption
  enabled_for_template_deployment = var.enabled_for_template_deployment
  location                        = var.location
  name                            = var.name
  public_network_access_enabled   = var.public_network_access_enabled
  purge_protection_enabled        = var.purge_protection_enabled
  resource_group_name             = var.resource_group_name
  sku_name                        = var.sku_name
  soft_delete_retention_days      = var.soft_delete_retention_days
  tags                            = var.tags
  tenant_id                       = var.tenant_id

  # This block is optional with no minimum number of items and no maximum number of items
  contact {
    email = var.contact_email
    name  = var.contact_name
    phone = var.contact_phone
  }

  # This block is optional with no minimum number of items and no maximum number of items
  network_acls {
    bypass                     = var.network_acls_bypass
    default_action             = var.network_acls_default_action
    ip_rules                   = var.network_acls_ip_rules
    virtual_network_subnet_ids = var.network_acls_virtual_network_subnet_ids
  }

  # This block is optional with no minimum number of items and no maximum number of items
  timeouts {
    create = var.timeouts_create
    delete = var.timeouts_delete
    read   = var.timeouts_read
    update = var.timeouts_update
  }
}

