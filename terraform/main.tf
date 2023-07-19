resource "aws_s3_bucket" "main" {
  bucket = "this-bucket"
}

resource "azurerm_virtual_network" "main" {
  address_space           = var.address_space
  bgp_community           = var.bgp_community
  dns_servers             = var.dns_servers
  edge_zone               = var.edge_zone
  flow_timeout_in_minutes = var.flow_timeout_in_minutes
  id                      = var.id
  location                = var.location
  name                    = var.name
  resource_group_name     = var.resource_group_name
  subnet                  = var.subnet
  tags                    = var.tags

  # This block is optional allowing for 0 to 1 item(s)
  ddos_protection_plan {
    enable = var.ddos_protection_plan_enable
    id     = var.ddos_protection_plan_id
  }

  # This block is optional allowing for 0 to N item(s)
  timeouts {
  }
}

resource "azurerm_resource_group" "main" {
  location = var.location
  name     = var.name
  tags     = var.tags
}