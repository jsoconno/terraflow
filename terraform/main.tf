resource "azurerm_management_lock" "main" {
  lock_level = var.lock_level
  name       = var.name
  scope      = var.scope
}

resource "resource_group" "main" {
  location = var.location # (Required) The Azure Region where the Resource Group should exist. Changing this forces a new Resource Group to be created.
  name     = var.name     # (Required) The Name which should be used for this Resource Group. Changing this forces a new Resource Group to be created.
}