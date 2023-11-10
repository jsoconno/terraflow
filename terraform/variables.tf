variable "resource_group_name" {
  description = "The name of the Resource Group where the AppService should exist. Changing this forces a new AppService to be created."
  type        = string
}

variable "tags" {
  type        = map(string)
  description = "A mapping of tags which should be assigned to the Resource Group."
  default     = {}
}

variable "location" {
  description = "The Azure Region where the Resource Group should exist. Changing this forces a new Resource Group to be created."
  type        = string
}

variable "name" {
  type        = string
  description = "The Name of this Resource Group."
}
