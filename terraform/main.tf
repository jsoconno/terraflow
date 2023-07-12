resource "azurerm_resource_group" "main" {
  location = var.location
  name     = var.name
  tags     = var.tags

  # This block is optional
  timeouts {
    create = var.timeouts_create
    delete = var.timeouts_delete
    read   = var.timeouts_read
    update = var.timeouts_update

  }
}