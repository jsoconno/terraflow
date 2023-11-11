# Terraform docs: https://github.com/hashicorp/terraform-provider-azurerm/blob/v3.45.0/website/docs/r/resource_group.html.markdown
# This resource creates an Azure resource group
resource "azurerm_resource_group" "main" {
  location = var.location               # The Azure Region where the Resource Group should exist. Changing this forces a new Resource Group to be created.
  name     = "rg-${var.app}-${var.env}" # The Name which should be used for this Resource Group. Changing this forces a new Resource Group to be created.
  tags     = var.tags                   # A mapping of tags which should be assigned to the Resource Group.
}