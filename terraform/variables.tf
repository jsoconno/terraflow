variable "enable_rbac_authorization" {
  type    = bool
  default = null
}

variable "enabled_for_deployment" {
  type    = bool
  default = null
}

variable "enabled_for_disk_encryption" {
  type    = bool
  default = null
}

variable "enabled_for_template_deployment" {
  type    = bool
  default = null
}

variable "location" {
  type = string
}

variable "name" {
  type        = string
  description = "(Required) Specifies the name of the Key Vault. Changing this forces a new resource to be created. The name must be globally unique. If the vault is in a recoverable state then the vault will need to be purged before reusing the name."
}

variable "public_network_access_enabled" {
  type    = bool
  default = null
}

variable "purge_protection_enabled" {
  type    = bool
  default = null
}

variable "resource_group_name" {
  type = string
}

variable "sku_name" {
  type = string
}

variable "soft_delete_retention_days" {
  type    = number
  default = null
}

variable "tags" {
  type    = map(string)
  default = null
}

variable "tenant_id" {
  type = string
}

variable "contact_email" {
  type = string
}

variable "contact_name" {
  type    = string
  default = null
}

variable "contact_phone" {
  type    = string
  default = null
}

variable "network_acls_bypass" {
  type = string
}

variable "network_acls_default_action" {
  type = string
}

variable "network_acls_ip_rules" {
  type    = set(string)
  default = null
}

variable "network_acls_virtual_network_subnet_ids" {
  type    = set(string)
  default = null
}

variable "timeouts_create" {
  type    = string
  default = null
}

variable "timeouts_delete" {
  type    = string
  default = null
}

variable "timeouts_read" {
  type    = string
  default = null
}

variable "timeouts_update" {
  type    = string
  default = null
}