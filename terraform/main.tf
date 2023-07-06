resource "azurerm_management_lock" "main" {
  lock_level = var.lock_level
  name       = var.name
  scope      = var.scope
}

resource "resource_group" "main" {
  location = var.location # (Required) The Azure Region where the Resource Group should exist. Changing this forces a new Resource Group to be created.
  name     = var.name     # (Required) The Name which should be used for this Resource Group. Changing this forces a new Resource Group to be created.
}

resource "windows_function_app" "main" {
  location            = var.location
  name                = var.name
  resource_group_name = var.resource_group_name
  service_plan_id     = var.service_plan_id

  # This block is required
  site_config {
  }
}

resource "virtual_network" "main" {
  address_space           = var.address_space
  bgp_community           = var.bgp_community
  edge_zone               = var.edge_zone
  flow_timeout_in_minutes = var.flow_timeout_in_minutes
  location                = var.location
  name                    = var.name
  resource_group_name     = var.resource_group_name
  tags                    = var.tags
}