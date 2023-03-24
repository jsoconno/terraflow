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

# Terraform docs: https://github.com/hashicorp/terraform-provider-azurerm/blob/main/website/docs/r/key_vault.html.markdown
resource "azurerm_key_vault" "main" {
  enable_rbac_authorization       = var.enable_rbac_authorization       # (Optional) Boolean flag to specify whether Azure Key Vault uses Role Based Access Control (RBAC) for authorization of data actions.
  enabled_for_deployment          = var.enabled_for_deployment          # (Optional) Boolean flag to specify whether Azure Virtual Machines are permitted to retrieve certificates stored as secrets from the key vault.
  enabled_for_disk_encryption     = var.enabled_for_disk_encryption     # (Optional) Boolean flag to specify whether Azure Disk Encryption is permitted to retrieve secrets from the vault and unwrap keys.
  enabled_for_template_deployment = var.enabled_for_template_deployment # (Optional) Boolean flag to specify whether Azure Resource Manager is permitted to retrieve secrets from the key vault.
  location                        = var.location                        # (Required) Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
  name                            = data.azurerm_key_vault.main.name    # (Required) Specifies the name of the Key Vault. Changing this forces a new resource to be created. The name must be globally unique. If the vault is in a recoverable state then the vault will need to be purged before reusing the name.
  public_network_access_enabled   = var.public_network_access_enabled   # (Optional) Whether public network access is allowed for this Key Vault. Defaults to true.
  purge_protection_enabled        = var.purge_protection_enabled        # (Optional) Is Purge Protection enabled for this Key Vault?
  resource_group_name             = var.resource_group_name             # (Required) The name of the resource group in which to create the Key Vault. Changing this forces a new resource to be created.
  sku_name                        = var.sku_name                        # (Required) The Name of the SKU used for this Key Vault. Possible values are standard and premium.
  soft_delete_retention_days      = var.soft_delete_retention_days      # (Optional) The number of days that items should be retained for once soft-deleted. This value can be between 7 and 90 (the default) days.
  tags                            = var.tags                            # (Optional) A mapping of tags to assign to the resource.
  tenant_id                       = var.tenant_id                       # (Required) The Azure Active Directory tenant ID that should be used for authenticating requests to the key vault.

  # This block is optional with no minimum number of items and no maximum number of items
  dynamic "contact" {
    for_each = var.contact
    content {
      email = contact.value["email"] # (Required) E-mail address of the contact.
      name  = contact.value["name"]  # (Optional) Name of the contact.
      phone = contact.value["phone"] # (Optional) Phone number of the contact.
    }
  }

  # This block is optional with no minimum number of items and no maximum number of items
  timeouts {
    create = timeouts_create # (Defaults to 30 minutes) Used when creating the Key Vault.
    delete = timeouts_delete # (Defaults to 30 minutes) Used when deleting the Key Vault.
    read   = timeouts_read   # (Defaults to 5 minutes) Used when retrieving the Key Vault.
    update = timeouts_update # (Defaults to 30 minutes) Used when updating the Key Vault.
  }
}



# Terraform docs: https://github.com/hashicorp/terraform-provider-azurerm/blob/main/website/docs/d/key_vault.html.markdown
data "azurerm_key_vault" "main" {
  name                = "hello"                 # Specifies the name of the Key Vault.
  resource_group_name = var.resource_group_name # The name of the Resource Group in which the Key Vault exists.

  # This block is optional with no minimum number of items and no maximum number of items
  timeouts {
    read = var.timeouts_read # (Defaults to 5 minutes) Used when retrieving the Key Vault.
  }
}

# Terraform docs: https://github.com/hashicorp/terraform-provider-azurerm/blob/main/website/docs/r/resource_group.html.markdown
resource "azurerm_resource_group" "main" {
  location = var.location # (Required) The Azure Region where the Resource Group should exist. Changing this forces a new Resource Group to be created.
  name     = var.name     # (Required) The Name which should be used for this Resource Group. Changing this forces a new Resource Group to be created.
  tags     = var.tags     # (Optional) A mapping of tags which should be assigned to the Resource Group.

  # This block is optional with no minimum number of items and no maximum number of items
  timeouts {
    create = var.timeouts_create # (Defaults to 90 minutes) Used when creating the Resource Group.
    delete = var.timeouts_delete # (Defaults to 90 minutes) Used when deleting the Resource Group.
    read   = var.timeouts_read   # (Defaults to 5 minutes) Used when retrieving the Resource Group.
    update = var.timeouts_update # (Defaults to 90 minutes) Used when updating the Resource Group.
  }
}