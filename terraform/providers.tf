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
  features {
    api_management {
      purge_soft_delete_on_destroy = var.purge_soft_delete_on_destroy
      recover_soft_deleted         = var.recover_soft_deleted
    }
    app_configuration {
      purge_soft_delete_on_destroy = var.purge_soft_delete_on_destroy
      recover_soft_deleted         = var.recover_soft_deleted
    }
    application_insights {
      disable_generated_rule = var.disable_generated_rule
    }
    cognitive_account {
      purge_soft_delete_on_destroy = var.purge_soft_delete_on_destroy
    }
    key_vault {
      purge_soft_delete_on_destroy                            = var.purge_soft_delete_on_destroy
      purge_soft_deleted_certificates_on_destroy              = var.purge_soft_deleted_certificates_on_destroy
      purge_soft_deleted_hardware_security_modules_on_destroy = var.purge_soft_deleted_hardware_security_modules_on_destroy
      purge_soft_deleted_keys_on_destroy                      = var.purge_soft_deleted_keys_on_destroy
      purge_soft_deleted_secrets_on_destroy                   = var.purge_soft_deleted_secrets_on_destroy
      recover_soft_deleted_certificates                       = var.recover_soft_deleted_certificates
      recover_soft_deleted_key_vaults                         = var.recover_soft_deleted_key_vaults
      recover_soft_deleted_keys                               = var.recover_soft_deleted_keys
      recover_soft_deleted_secrets                            = var.recover_soft_deleted_secrets
    }
    log_analytics_workspace {
      permanently_delete_on_destroy = var.permanently_delete_on_destroy
    }
    managed_disk {
      expand_without_downtime = var.expand_without_downtime
    }
    network {
      relaxed_locking = var.relaxed_locking
    }
    resource_group {
      prevent_deletion_if_contains_resources = var.prevent_deletion_if_contains_resources
    }
    template_deployment {
      delete_nested_items_during_deletion = var.delete_nested_items_during_deletion
    }
    virtual_machine {
      delete_os_disk_on_deletion     = var.delete_os_disk_on_deletion
      graceful_shutdown              = var.graceful_shutdown
      skip_shutdown_and_force_delete = var.skip_shutdown_and_force_delete
    }
    virtual_machine_scale_set {
      force_delete                  = var.force_delete
      roll_instances_when_required  = var.roll_instances_when_required
      scale_to_zero_before_deletion = var.scale_to_zero_before_deletion
    }
  }
}