provider "azurerm" {
  auxiliary_tenant_ids           = var.auxiliary_tenant_ids
  client_certificate             = var.client_certificate
  client_certificate_password    = var.client_certificate_password
  client_certificate_path        = var.client_certificate_path
  client_id                      = var.client_id
  client_secret                  = var.client_secret
  disable_correlation_request_id = var.disable_correlation_request_id
  disable_terraform_partner_id   = var.disable_terraform_partner_id
  environment                    = var.environment
  metadata_host                  = var.metadata_host
  msi_endpoint                   = var.msi_endpoint
  oidc_request_token             = var.oidc_request_token
  oidc_request_url               = var.oidc_request_url
  oidc_token                     = var.oidc_token
  oidc_token_file_path           = var.oidc_token_file_path
  partner_id                     = var.partner_id
  skip_provider_registration     = var.skip_provider_registration
  storage_use_azuread            = var.storage_use_azuread
  subscription_id                = var.subscription_id
  tenant_id                      = var.tenant_id
  use_cli                        = var.use_cli
  use_msi                        = var.use_msi
  use_oidc                       = var.use_oidc

  # This block is required with a minimum of 1 items and a maximum of 1 items
  features {
  }
}