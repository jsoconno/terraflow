variable "tags" {
  description = "A mapping of tags which should be assigned to the Resource Group."
  default     = {}
  type        = map(any)
}

variable "location" {
  description = "The Azure Region where the Resource Group should exist. Changing this forces a new Resource Group to be created."
  type        = string
}