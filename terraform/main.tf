resource "azurerm_management_lock" "main" {
  lock_level = var.lock_level
  name       = var.name
  notes      = var.notes
  scope      = var.scope
}