data "azurerm_key_vault" "main" {
  name                = var.test_name
  resource_group_name = var.test_resource_group_name

  # This block is optional with no minimum number of items and no maximum number of items
  timeouts {
    read = var.test_timeouts_read
  }
}