resource "azurerm_key_vault" "main" {
  location            = var.location
  name                = var.name
  resource_group_name = var.resource_group_name
  sku_name            = var.sku_name
  tenant_id           = var.tenant_id
}