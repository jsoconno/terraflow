data "key_vault" "main" {
  name                = var.name                # (Required) Specifies the name of the Key Vault. Changing this forces a new resource to be created. The name must be globally unique. If the vault is in a recoverable state then the vault will need to be purged before reusing the name.
  resource_group_name = var.resource_group_name # (Required) The name of the resource group in which to create the Key Vault. Changing this forces a new resource to be created.
  timeouts {
    read = var.read # (Defaults to 5 minutes) Used when retrieving the Key Vault.
  }
}