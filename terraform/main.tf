resource "azurerm_resource_group" "main" {
  location = var.resource_group_location
  name     = var.resource_group_name
  tags     = var.resource_group_tags

  # This block is optional allowing for 0 to N item(s)
  timeouts {
    create = var.resource_group_timeouts_create
    delete = var.resource_group_timeouts_delete
    read   = var.resource_group_timeouts_read
    update = var.resource_group_timeouts_update
  }
}