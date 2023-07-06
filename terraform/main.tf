resource "azurerm_management_lock" "main" {
  lock_level = var.lock_level
  name       = var.name
  scope      = var.scope
}