# Terraform docs: https://github.com/hashicorp/terraform-provider-azurerm/blob/v3.45.0/website/docs/r/resource_group.html.markdown
# This resource creates an Azure Resource Group.
resource "resource_group" "main" {
  location = var.location
  name     = var.name
  tags     = var.tags
}