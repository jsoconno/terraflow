variable "location" {
  type        = string
  description = "(Required) Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created."
}

variable "name" {
  type        = string
  description = "(Required) Specifies the name of the Key Vault. Changing this forces a new resource to be created. The name must be globally unique. If the vault is in a recoverable state then the vault will need to be purged before reusing the name."
}

variable "resource_group_name" {
  type        = string
  description = "(Required) The name of the resource group in which to create the Key Vault. Changing this forces a new resource to be created."
}

variable "sku_name" {
  type        = string
  description = "(Required) The Name of the SKU used for this Key Vault. Possible values are standard and premium."
}

variable "tenant_id" {
  type        = string
  description = "(Required) The Azure Active Directory tenant ID that should be used for authenticating requests to the key vault."
}