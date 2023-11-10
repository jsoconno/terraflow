resource "azurerm_service_plan" "main" {
  app_service_environment_id   = var.app_service_environment_id
  location                     = var.location
  maximum_elastic_worker_count = var.maximum_elastic_worker_count
  name                         = var.name
  os_type                      = var.os_type
  per_site_scaling_enabled     = var.per_site_scaling_enabled
  resource_group_name          = var.resource_group_name
  sku_name                     = var.sku_name
  tags                         = var.tags
  worker_count                 = var.worker_count
  zone_balancing_enabled       = var.zone_balancing_enabled
}

resource "azurerm_resource_group" "main" {
  location = var.location
  name     = var.name
  tags     = var.tags
}