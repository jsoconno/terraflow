variable "location" {
  type        = string
  description = "The Azure region where resources should be deployed. Changing this will create new resources"
  default     = "eastus"
}

variable "tags" {
  type        = map(string)
  description = "Tags to apply to the Azure resource(s)."
}

variable "app" {
  type = string
}

variable "env" {
  type = string
}
