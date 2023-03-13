resource "azurerm_resource_group" "data_center" {
  location = var.test_location # (Required) The Azure Region where the Resource Group should exist. Changing this forces a new Resource Group to be created.
  name     = "test this out"   # (Required) The Name which should be used for this Resource Group. Changing this forces a new Resource Group to be created.
}