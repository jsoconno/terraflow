resource "key_vault" "main" {
  enable_rbac_authorization       = var.enable_rbac_authorization       # (Optional) Boolean flag to specify whether Azure Key Vault uses Role Based Access Control (RBAC) for authorization of data actions.
  enabled_for_deployment          = var.enabled_for_deployment          # (Optional) Boolean flag to specify whether Azure Virtual Machines are permitted to retrieve certificates stored as secrets from the key vault.
  enabled_for_disk_encryption     = var.enabled_for_disk_encryption     # (Optional) Boolean flag to specify whether Azure Disk Encryption is permitted to retrieve secrets from the vault and unwrap keys.
  enabled_for_template_deployment = var.enabled_for_template_deployment # (Optional) Boolean flag to specify whether Azure Resource Manager is permitted to retrieve secrets from the key vault.
  location                        = var.location                        # (Required) Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
  name                            = var.name                            # (Required) Specifies the name of the Key Vault. Changing this forces a new resource to be created. The name must be globally unique. If the vault is in a recoverable state then the vault will need to be purged before reusing the name.
  public_network_access_enabled   = var.public_network_access_enabled   # (Optional) Whether public network access is allowed for this Key Vault. Defaults to true.
  purge_protection_enabled        = var.purge_protection_enabled        # (Optional) Is Purge Protection enabled for this Key Vault?
  resource_group_name             = var.resource_group_name             # (Required) The name of the resource group in which to create the Key Vault. Changing this forces a new resource to be created.
  sku_name                        = var.sku_name                        # (Required) The Name of the SKU used for this Key Vault. Possible values are standard and premium.
  soft_delete_retention_days      = var.soft_delete_retention_days      # (Optional) The number of days that items should be retained for once soft-deleted. This value can be between 7 and 90 (the default) days.
  tags                            = var.tags                            # (Optional) A mapping of tags to assign to the resource.
  tenant_id                       = var.tenant_id                       # (Required) The Azure Active Directory tenant ID that should be used for authenticating requests to the key vault.

  # This block is optional with no minimum number of items and no maximum number of items
  contact {
    email = var.contact_email # (Required) E-mail address of the contact.
    name  = var.contact_name  # (Optional) Name of the contact.
    phone = var.contact_phone # (Optional) Phone number of the contact.
  }

  # This block is optional with no minimum number of items and no maximum number of items
  network_acls {
    bypass                     = var.network_acls_bypass                     # (Required) Specifies which traffic can bypass the network rules. Possible values are AzureServices and None.
    default_action             = var.network_acls_default_action             # (Required) The Default Action to use when no rules match from ip_rules / virtual_network_subnet_ids. Possible values are Allow and Deny.
    ip_rules                   = var.network_acls_ip_rules                   # (Optional) One or more IP Addresses, or CIDR Blocks which should be able to access the Key Vault.
    virtual_network_subnet_ids = var.network_acls_virtual_network_subnet_ids # (Optional) One or more Subnet IDs which should be able to access this Key Vault.
  }

  # This block is optional with no minimum number of items and no maximum number of items
  timeouts {
    create = var.timeouts_create # (Defaults to 30 minutes) Used when creating the Key Vault.
    delete = var.timeouts_delete # (Defaults to 30 minutes) Used when deleting the Key Vault.
    read   = var.timeouts_read   # (Defaults to 5 minutes) Used when retrieving the Key Vault.
    update = var.timeouts_update # (Defaults to 30 minutes) Used when updating the Key Vault.
  }
}