resource "azurerm_resource_group" "main" {
  location = var.location
  name     = var.name
  tags     = var.tags

  # This block is optional
  timeouts {
    create = var.timeouts_create
    delete = var.timeouts_delete
    read   = var.timeouts_read
    update = var.timeouts_update

  }
}

resource "key_vault" "main" {
  enable_rbac_authorization       = var.test_enable_rbac_authorization
  enabled_for_deployment          = var.test_enabled_for_deployment
  enabled_for_disk_encryption     = var.test_enabled_for_disk_encryption
  enabled_for_template_deployment = var.test_enabled_for_template_deployment
  location                        = "westus"
  name                            = var.test_name
  public_network_access_enabled   = var.test_public_network_access_enabled
  purge_protection_enabled        = var.test_purge_protection_enabled
  resource_group_name             = var.test_resource_group_name
  sku_name                        = var.test_sku_name
  soft_delete_retention_days      = var.test_soft_delete_retention_days
  tags                            = var.test_tags
  tenant_id                       = var.test_tenant_id

  # This block is optional
  contact {
    email = var.test_contact_email
    name  = var.test_contact_name
    phone = var.test_contact_phone

  }

  # This block is optional
  network_acls {
    bypass                     = var.test_network_acls_bypass
    default_action             = var.test_network_acls_default_action
    ip_rules                   = var.test_network_acls_ip_rules
    virtual_network_subnet_ids = var.test_network_acls_virtual_network_subnet_ids

  }
}