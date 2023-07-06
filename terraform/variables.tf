variable "lock_level" {
  type        = string
  description = "(Required) Specifies the Level to be used for this Lock. Possible values are CanNotDelete and ReadOnly. Changing this forces a new resource to be created."
}

variable "name" {
  type        = string
  description = "(Required) Specifies the name of the Management Lock. Changing this forces a new resource to be created."
}

variable "scope" {
  type        = string
  description = "(Required) Specifies the scope at which the Management Lock should be created. Changing this forces a new resource to be created."
}