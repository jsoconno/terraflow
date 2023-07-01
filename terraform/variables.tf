variable "enable_rbac_authorization" {
  type        = bool
  description = "(Optional) Boolean flag to specify whether Azure Key Vault uses Role Based Access Control (RBAC) for authorization of data actions."
  default     = null
}

variable "enabled_for_deployment" {
  type        = bool
  description = "(Optional) Boolean flag to specify whether Azure Virtual Machines are permitted to retrieve certificates stored as secrets from the key vault."
  default     = null
}

variable "enabled_for_disk_encryption" {
  type        = bool
  description = "(Optional) Boolean flag to specify whether Azure Disk Encryption is permitted to retrieve secrets from the vault and unwrap keys."
  default     = null
}

variable "enabled_for_template_deployment" {
  type        = bool
  description = "(Optional) Boolean flag to specify whether Azure Resource Manager is permitted to retrieve secrets from the key vault."
  default     = null
}

variable "location" {
  type        = string
  description = "(Required) Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created."
}

variable "name" {
  type        = string
  description = "(Required) Specifies the name of the Key Vault. Changing this forces a new resource to be created. The name must be globally unique. If the vault is in a recoverable state then the vault will need to be purged before reusing the name."
}

variable "public_network_access_enabled" {
  type        = bool
  description = "(Optional) Whether public network access is allowed for this Key Vault. Defaults to true."
  default     = null
}

variable "purge_protection_enabled" {
  type        = bool
  description = "(Optional) Is Purge Protection enabled for this Key Vault?"
  default     = null
}

variable "resource_group_name" {
  type        = string
  description = "(Required) The name of the resource group in which to create the Key Vault. Changing this forces a new resource to be created."
}

variable "sku_name" {
  type        = string
  description = "(Required) The Name of the SKU used for this Key Vault. Possible values are standard and premium."
}

variable "soft_delete_retention_days" {
  type        = number
  description = "(Optional) The number of days that items should be retained for once soft-deleted. This value can be between 7 and 90 (the default) days."
  default     = null
}

variable "tags" {
  type        = map(string)
  description = "(Optional) A mapping of tags to assign to the resource."
  default     = null
}

variable "tenant_id" {
  type        = string
  description = "(Required) The Azure Active Directory tenant ID that should be used for authenticating requests to the key vault."
}

variable "contact_email" {
  type        = string
  description = "(Required) E-mail address of the contact."
}

variable "contact_name" {
  type        = string
  description = "(Optional) Name of the contact."
  default     = null
}

variable "contact_phone" {
  type        = string
  description = "(Optional) Phone number of the contact."
  default     = null
}

variable "network_acls_bypass" {
  type        = string
  description = "(Required) Specifies which traffic can bypass the network rules. Possible values are AzureServices and None."
}

variable "network_acls_default_action" {
  type        = string
  description = "(Required) The Default Action to use when no rules match from ip_rules / virtual_network_subnet_ids. Possible values are Allow and Deny."
}

variable "network_acls_ip_rules" {
  type        = set(string)
  description = "(Optional) One or more IP Addresses, or CIDR Blocks which should be able to access the Key Vault."
  default     = null
}

variable "network_acls_virtual_network_subnet_ids" {
  type        = set(string)
  description = "(Optional) One or more Subnet IDs which should be able to access this Key Vault."
  default     = null
}

variable "timeouts_create" {
  type        = string
  description = "(Defaults to 30 minutes) Used when creating the Key Vault."
  default     = null
}

variable "timeouts_delete" {
  type        = string
  description = "(Defaults to 30 minutes) Used when deleting the Key Vault."
  default     = null
}

variable "timeouts_read" {
  type        = string
  description = "(Defaults to 5 minutes) Used when retrieving the Key Vault."
  default     = null
}

variable "timeouts_update" {
  type        = string
  description = "(Defaults to 30 minutes) Used when updating the Key Vault."
  default     = null
}