resource "azurerm_resource_group" "main" {
  location = var.role_assignment_location
  name     = "test"
  tags     = var.role_assignment_tags
}

resource "azurerm_resource_group" "other" {
  location = var.role_assignment_location
  name     = "test"
  tags     = var.role_assignment_tags
}

