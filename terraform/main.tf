resource "key_vault" "test" {
  enable_rbac_authorization       = var.xxx_enable_rbac_authorization
  enabled_for_deployment          = var.xxx_enabled_for_deployment
  enabled_for_disk_encryption     = var.xxx_enabled_for_disk_encryption
  enabled_for_template_deployment = var.xxx_enabled_for_template_deployment
  location                        = var.xxx_location
  name                            = "my-kv"
  public_network_access_enabled   = var.xxx_public_network_access_enabled
  purge_protection_enabled        = var.xxx_purge_protection_enabled
  resource_group_name             = var.xxx_resource_group_name
  sku_name                        = var.xxx_sku_name
  soft_delete_retention_days      = var.xxx_soft_delete_retention_days
  tenant_id                       = var.xxx_tenant_id
  contact {
    email = var.xxx_email
    name  = "my-kv"
    phone = var.xxx_phone
  }
  network_acls {
    bypass                     = var.xxx_bypass
    default_action             = var.xxx_default_action
    ip_rules                   = var.xxx_ip_rules
    virtual_network_subnet_ids = var.xxx_virtual_network_subnet_ids
  }
}

data "key_vault" "test" {
  name                = "my-kv"                     # (Required) Specifies the name of the Key Vault. Changing this forces a new resource to be created. The name must be globally unique. If the vault is in a recoverable state then the vault will need to be purged before reusing the name.
  resource_group_name = var.xxx_resource_group_name # (Required) The name of the resource group in which to create the Key Vault. Changing this forces a new resource to be created.
}