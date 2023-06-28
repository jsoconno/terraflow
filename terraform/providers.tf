provider "azurerm" {
  auxiliary_tenant_ids           = var.auxiliary_tenant_ids           # No description
  client_certificate             = var.client_certificate             # Base64 encoded PKCS#12 certificate bundle to use when authenticating as a Service Principal using a Client Certificate
  client_certificate_password    = var.client_certificate_password    # The password associated with the Client Certificate. For use when authenticating as a Service Principal using a Client Certificate
  client_certificate_path        = var.client_certificate_path        # The path to the Client Certificate associated with the Service Principal for use when authenticating as a Service Principal using a Client Certificate.
  client_id                      = var.client_id                      # The Client ID which should be used.
  client_secret                  = var.client_secret                  # The Client Secret which should be used. For use When authenticating as a Service Principal using a Client Secret.
  disable_correlation_request_id = var.disable_correlation_request_id # This will disable the x-ms-correlation-request-id header.
  disable_terraform_partner_id   = var.disable_terraform_partner_id   # This will disable the Terraform Partner ID which is used if a custom `partner_id` isn't specified.
  environment                    = var.environment                    # The Cloud Environment which should be used. Possible values are public, usgovernment, and china. Defaults to public.
  metadata_host                  = var.metadata_host                  # The Hostname which should be used for the Azure Metadata Service.
  msi_endpoint                   = var.msi_endpoint                   # The path to a custom endpoint for Managed Service Identity - in most circumstances this should be detected automatically. 
  oidc_request_token             = var.oidc_request_token             # The bearer token for the request to the OIDC provider. For use when authenticating as a Service Principal using OpenID Connect.
  oidc_request_url               = var.oidc_request_url               # The URL for the OIDC provider from which to request an ID token. For use when authenticating as a Service Principal using OpenID Connect.
  oidc_token                     = var.oidc_token                     # The OIDC ID token for use when authenticating as a Service Principal using OpenID Connect.
  oidc_token_file_path           = var.oidc_token_file_path           # The path to a file containing an OIDC ID token for use when authenticating as a Service Principal using OpenID Connect.
  partner_id                     = var.partner_id                     # A GUID/UUID that is registered with Microsoft to facilitate partner resource usage attribution.
  skip_provider_registration     = var.skip_provider_registration     # Should the AzureRM Provider skip registering all of the Resource Providers that it supports, if they're not already registered?
  storage_use_azuread            = var.storage_use_azuread            # Should the AzureRM Provider use AzureAD to access the Storage Data Plane API's?
  subscription_id                = var.subscription_id                # The Subscription ID which should be used.
  tenant_id                      = var.tenant_id                      # The Tenant ID which should be used.
  use_cli                        = var.use_cli                        # Allow Azure CLI to be used for Authentication.
  use_msi                        = var.use_msi                        # Allow Managed Service Identity to be used for Authentication.
  use_oidc                       = var.use_oidc                       # Allow OpenID Connect to be used for authentication

  # This block is required
  features {

    # This block is optional
    api_management {
      purge_soft_delete_on_destroy = var.purge_soft_delete_on_destroy # No description
      recover_soft_deleted         = var.recover_soft_deleted         # No description
    }

    # This block is optional
    app_configuration {
      purge_soft_delete_on_destroy = var.purge_soft_delete_on_destroy # No description
      recover_soft_deleted         = var.recover_soft_deleted         # No description
    }

    # This block is optional
    application_insights {
      disable_generated_rule = var.disable_generated_rule # No description
    }

    # This block is optional
    cognitive_account {
      purge_soft_delete_on_destroy = var.purge_soft_delete_on_destroy # No description
    }

    # This block is optional
    key_vault {
      purge_soft_delete_on_destroy                            = var.purge_soft_delete_on_destroy                            # When enabled soft-deleted `azurerm_key_vault` resources will be permanently deleted (e.g purged), when destroyed
      purge_soft_deleted_certificates_on_destroy              = var.purge_soft_deleted_certificates_on_destroy              # When enabled soft-deleted `azurerm_key_vault_certificate` resources will be permanently deleted (e.g purged), when destroyed
      purge_soft_deleted_hardware_security_modules_on_destroy = var.purge_soft_deleted_hardware_security_modules_on_destroy # When enabled soft-deleted `azurerm_key_vault_managed_hardware_security_module` resources will be permanently deleted (e.g purged), when destroyed
      purge_soft_deleted_keys_on_destroy                      = var.purge_soft_deleted_keys_on_destroy                      # When enabled soft-deleted `azurerm_key_vault_key` resources will be permanently deleted (e.g purged), when destroyed
      purge_soft_deleted_secrets_on_destroy                   = var.purge_soft_deleted_secrets_on_destroy                   # When enabled soft-deleted `azurerm_key_vault_secret` resources will be permanently deleted (e.g purged), when destroyed
      recover_soft_deleted_certificates                       = var.recover_soft_deleted_certificates                       # When enabled soft-deleted `azurerm_key_vault_certificate` resources will be restored, instead of creating new ones
      recover_soft_deleted_key_vaults                         = var.recover_soft_deleted_key_vaults                         # When enabled soft-deleted `azurerm_key_vault` resources will be restored, instead of creating new ones
      recover_soft_deleted_keys                               = var.recover_soft_deleted_keys                               # When enabled soft-deleted `azurerm_key_vault_key` resources will be restored, instead of creating new ones
      recover_soft_deleted_secrets                            = var.recover_soft_deleted_secrets                            # When enabled soft-deleted `azurerm_key_vault_secret` resources will be restored, instead of creating new ones
    }

    # This block is optional
    log_analytics_workspace {
      permanently_delete_on_destroy = var.permanently_delete_on_destroy # No description
    }

    # This block is optional
    managed_disk {
      expand_without_downtime = var.expand_without_downtime # No description
    }

    # This block is optional
    network {
      relaxed_locking = var.relaxed_locking # No description
    }

    # This block is optional
    resource_group {
      prevent_deletion_if_contains_resources = var.prevent_deletion_if_contains_resources # No description
    }

    # This block is optional
    template_deployment {
      delete_nested_items_during_deletion = var.delete_nested_items_during_deletion # No description
    }

    # This block is optional
    virtual_machine {
      delete_os_disk_on_deletion     = var.delete_os_disk_on_deletion     # No description
      graceful_shutdown              = var.graceful_shutdown              # No description
      skip_shutdown_and_force_delete = var.skip_shutdown_and_force_delete # No description
    }

    # This block is optional
    virtual_machine_scale_set {
      force_delete                  = var.force_delete                  # No description
      roll_instances_when_required  = var.roll_instances_when_required  # No description
      scale_to_zero_before_deletion = var.scale_to_zero_before_deletion # No description
    }
  }
}