/**
 * # Main title
 *
 * Everything in this comment block will get extracted into docs.
 *
 * You can put simple text or complete Markdown content
 * here. Subsequently if you want to render AsciiDoc format
 * you can put AsciiDoc compatible content in this comment
 * block.
 */

provider "azurerm" {
  auxiliary_tenant_ids           = var.auxiliary_tenant_ids
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

  # This block is required with a minimum of 1 items and a maximum of 1 items
  features {

    # This block is optional with no minimum number of items and a maximum of 1 items
    api_management {
      purge_soft_delete_on_destroy = var.features_api_management_purge_soft_delete_on_destroy
      recover_soft_deleted         = var.features_api_management_recover_soft_deleted
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    app_configuration {
      purge_soft_delete_on_destroy = var.features_app_configuration_purge_soft_delete_on_destroy
      recover_soft_deleted         = var.features_app_configuration_recover_soft_deleted
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    application_insights {
      disable_generated_rule = var.features_application_insights_disable_generated_rule
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    cognitive_account {
      purge_soft_delete_on_destroy = var.features_cognitive_account_purge_soft_delete_on_destroy
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    key_vault {
      purge_soft_delete_on_destroy                            = var.features_key_vault_purge_soft_delete_on_destroy                            # When enabled soft-deleted `azurerm_key_vault` resources will be permanently deleted (e.g purged), when destroyed
      purge_soft_deleted_certificates_on_destroy              = var.features_key_vault_purge_soft_deleted_certificates_on_destroy              # When enabled soft-deleted `azurerm_key_vault_certificate` resources will be permanently deleted (e.g purged), when destroyed
      purge_soft_deleted_hardware_security_modules_on_destroy = var.features_key_vault_purge_soft_deleted_hardware_security_modules_on_destroy # When enabled soft-deleted `azurerm_key_vault_managed_hardware_security_module` resources will be permanently deleted (e.g purged), when destroyed
      purge_soft_deleted_keys_on_destroy                      = var.features_key_vault_purge_soft_deleted_keys_on_destroy                      # When enabled soft-deleted `azurerm_key_vault_key` resources will be permanently deleted (e.g purged), when destroyed
      purge_soft_deleted_secrets_on_destroy                   = var.features_key_vault_purge_soft_deleted_secrets_on_destroy                   # When enabled soft-deleted `azurerm_key_vault_secret` resources will be permanently deleted (e.g purged), when destroyed
      recover_soft_deleted_certificates                       = var.features_key_vault_recover_soft_deleted_certificates                       # When enabled soft-deleted `azurerm_key_vault_certificate` resources will be restored, instead of creating new ones
      recover_soft_deleted_key_vaults                         = var.features_key_vault_recover_soft_deleted_key_vaults                         # When enabled soft-deleted `azurerm_key_vault` resources will be restored, instead of creating new ones
      recover_soft_deleted_keys                               = var.features_key_vault_recover_soft_deleted_keys                               # When enabled soft-deleted `azurerm_key_vault_key` resources will be restored, instead of creating new ones
      recover_soft_deleted_secrets                            = var.features_key_vault_recover_soft_deleted_secrets                            # When enabled soft-deleted `azurerm_key_vault_secret` resources will be restored, instead of creating new ones
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    log_analytics_workspace {
      permanently_delete_on_destroy = var.features_log_analytics_workspace_permanently_delete_on_destroy
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    managed_disk {
      expand_without_downtime = var.features_managed_disk_expand_without_downtime
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    network {
      relaxed_locking = var.features_network_relaxed_locking
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    resource_group {
      prevent_deletion_if_contains_resources = var.features_resource_group_prevent_deletion_if_contains_resources
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    template_deployment {
      delete_nested_items_during_deletion = var.features_template_deployment_delete_nested_items_during_deletion
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    virtual_machine {
      delete_os_disk_on_deletion     = var.features_virtual_machine_delete_os_disk_on_deletion
      graceful_shutdown              = var.features_virtual_machine_graceful_shutdown
      skip_shutdown_and_force_delete = var.features_virtual_machine_skip_shutdown_and_force_delete
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    virtual_machine_scale_set {
      force_delete                  = var.features_virtual_machine_scale_set_force_delete
      roll_instances_when_required  = var.features_virtual_machine_scale_set_roll_instances_when_required
      scale_to_zero_before_deletion = var.features_virtual_machine_scale_set_scale_to_zero_before_deletion
    }
  }
}

# Terraform docs: https://github.com/hashicorp/terraform-provider-azurerm/blob/main/website/docs/r/resource_group.html.markdown
resource "azurerm_resource_group" "main" {
  location = var.location # (Required) The Azure Region where the Resource Group should exist. Changing this forces a new Resource Group to be created.
  name     = var.name     # (Required) The Name which should be used for this Resource Group. Changing this forces a new Resource Group to be created.
  tags     = var.tags     # (Optional) A mapping of tags which should be assigned to the Resource Group.

  # This block is optional with no minimum number of items and no maximum number of items
  timeouts {
    create = var.timeouts_create # (Defaults to 90 minutes) Used when creating the Resource Group.
    delete = var.timeouts_delete # (Defaults to 90 minutes) Used when deleting the Resource Group.
    read   = var.timeouts_read   # (Defaults to 5 minutes) Used when retrieving the Resource Group.
    update = var.timeouts_update # (Defaults to 90 minutes) Used when updating the Resource Group.
  }
}