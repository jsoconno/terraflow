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

resource "azurerm_resource_group" "other" {
  location = var.location
  name     = var.name
}

resource "azurerm_key_vault" "main" {
  location            = var.location
  name                = var.name
  resource_group_name = var.resource_group_name
  sku_name            = var.sku_name
  tenant_id           = var.tenant_id
}

resource "azurerm_storage_account" "main" {
  account_kind                      = var.account_kind                      # (Optional) Defines the Kind of account. Valid options are BlobStorage, BlockBlobStorage, FileStorage, Storage and StorageV2. Defaults to StorageV2.
  account_replication_type          = var.account_replication_type          # (Required) Defines the type of replication to use for this storage account. Valid options are LRS, GRS, RAGRS, ZRS, GZRS and RAGZRS.
  account_tier                      = var.account_tier                      # (Required) Defines the Tier to use for this storage account. Valid options are Standard and Premium. For BlockBlobStorage and FileStorage accounts only Premium is valid. Changing this forces a new resource to be created.
  allow_nested_items_to_be_public   = var.allow_nested_items_to_be_public   # (Optional) Allow or disallow nested items within this Account to opt into being public. Defaults to true.
  allowed_copy_scope                = var.allowed_copy_scope                # (Optional) Restrict copy to and from Storage Accounts within an AAD tenant or with Private Links to the same VNet. Possible values are AAD and PrivateLink.
  cross_tenant_replication_enabled  = var.cross_tenant_replication_enabled  # (Optional) Should cross Tenant replication be enabled? Defaults to true.
  default_to_oauth_authentication   = var.default_to_oauth_authentication   # (Optional) Default to Azure Active Directory authorization in the Azure portal when accessing the Storage Account. The default value is false
  edge_zone                         = var.edge_zone                         # (Optional) Specifies the Edge Zone within the Azure Region where this Storage Account should exist. Changing this forces a new Storage Account to be created.
  enable_https_traffic_only         = var.enable_https_traffic_only         # (Optional) Boolean flag which forces HTTPS if enabled, see here for more information. Defaults to true.
  infrastructure_encryption_enabled = var.infrastructure_encryption_enabled # (Optional) Is infrastructure encryption enabled? Changing this forces a new resource to be created. Defaults to false.
  is_hns_enabled                    = var.is_hns_enabled                    # (Optional) Is Hierarchical Namespace enabled? This can be used with Azure Data Lake Storage Gen 2 (see here for more information). Changing this forces a new resource to be created.
  location                          = var.location                          # (Required) Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
  min_tls_version                   = var.min_tls_version                   # (Optional) The minimum supported TLS version for the storage account. Possible values are TLS1_0, TLS1_1, and TLS1_2. Defaults to TLS1_2 for new storage accounts.
  name                              = var.name                              # (Required) Specifies the name of the storage account. Only lowercase Alphanumeric characters allowed. Changing this forces a new resource to be created. This must be unique across the entire Azure service, not just within the resource group.
  nfsv3_enabled                     = var.nfsv3_enabled                     # (Optional) Is NFSv3 protocol enabled? Changing this forces a new resource to be created. Defaults to false.
  public_network_access_enabled     = var.public_network_access_enabled     # (Optional) Whether the public network access is enabled? Defaults to true.
  queue_encryption_key_type         = var.queue_encryption_key_type         # (Optional) The encryption type of the queue service. Possible values are Service and Account. Changing this forces a new resource to be created. Default value is Service.
  resource_group_name               = var.resource_group_name               # (Required) The name of the resource group in which to create the storage account. Changing this forces a new resource to be created.
  sftp_enabled                      = var.sftp_enabled                      # (Optional) Boolean, enable SFTP for the storage account
  shared_access_key_enabled         = var.shared_access_key_enabled         # (Optional) Indicates whether the storage account permits requests to be authorized with the account access key via Shared Key. If false, then all requests, including shared access signatures, must be authorized with Azure Active Directory (Azure AD). The default value is true.
  table_encryption_key_type         = var.table_encryption_key_type         # (Optional) The encryption type of the table service. Possible values are Service and Account. Changing this forces a new resource to be created. Default value is Service.
  tags                              = var.tags                              # (Optional) A mapping of tags to assign to the resource.

  # This block is optional with no minimum number of items and no maximum number of items
  azure_files_authentication {
    directory_type = azure_files_authentication_directory_type # (Required) Specifies the directory service used. Possible values are AADDS, AD and AADKERB.

    # This block is optional with no minimum number of items and a maximum of 1 items
    dynamic "active_directory" {
      for_each = var.azure_files_authentication_active_directory
      content {
        domain_guid         = azure_files_authentication_active_directory.value["domain_guid"]         # (Required) Specifies the domain GUID.
        domain_name         = azure_files_authentication_active_directory.value["domain_name"]         # (Required) Specifies the primary domain that the AD DNS server is authoritative for.
        domain_sid          = azure_files_authentication_active_directory.value["domain_sid"]          # (Required) Specifies the security identifier (SID).
        forest_name         = azure_files_authentication_active_directory.value["forest_name"]         # (Required) Specifies the Active Directory forest.
        netbios_domain_name = azure_files_authentication_active_directory.value["netbios_domain_name"] # (Required) Specifies the NetBIOS domain name.
        storage_sid         = azure_files_authentication_active_directory.value["storage_sid"]         # (Required) Specifies the security identifier (SID) for Azure Storage.
      }
    }
  }

  # This block is optional with no minimum number of items and no maximum number of items
  blob_properties {
    change_feed_enabled           = blob_properties_change_feed_enabled           # (Optional) Is the blob service properties for change feed events enabled? Default to false.
    change_feed_retention_in_days = blob_properties_change_feed_retention_in_days # (Optional) The duration of change feed events retention in days. The possible values are between 1 and 146000 days (400 years). Setting this to null (or omit this in the configuration file) indicates an infinite retention of the change feed.
    last_access_time_enabled      = blob_properties_last_access_time_enabled      # (Optional) Is the last access time based tracking enabled? Default to false.
    versioning_enabled            = blob_properties_versioning_enabled            # (Optional) Is versioning enabled? Default to false.

    # This block is optional with no minimum number of items and a maximum of 1 items
    container_delete_retention_policy {
      days = blob_properties_container_delete_retention_policy_days # (Optional) Specifies the number of days that the container should be retained, between 1 and 365 days. Defaults to 7.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    cors_rule {
      allowed_headers    = blob_properties_cors_rule_allowed_headers    # (Required) A list of headers that are allowed to be a part of the cross-origin request.
      allowed_methods    = blob_properties_cors_rule_allowed_methods    # (Required) A list of HTTP methods that are allowed to be executed by the origin. Valid options are
      allowed_origins    = blob_properties_cors_rule_allowed_origins    # (Required) A list of origin domains that will be allowed by CORS.
      exposed_headers    = blob_properties_cors_rule_exposed_headers    # (Required) A list of response headers that are exposed to CORS clients.
      max_age_in_seconds = blob_properties_cors_rule_max_age_in_seconds # (Required) The number of seconds the client should cache a preflight response.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    delete_retention_policy {
      days = blob_properties_delete_retention_policy_days # (Required) Specifies the number of days that the blob can be restored, between 1 and 365 days. This must be less than the days specified for delete_retention_policy.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    restore_policy {
      days = blob_properties_restore_policy_days # (Optional) Specifies the number of days that the azurerm_storage_share should be retained, between 1 and 365 days. Defaults to 7.
    }
  }

  # This block is optional with no minimum number of items and no maximum number of items
  custom_domain {
    name          = custom_domain_name          # (Required) The Custom Domain Name to use for the Storage Account, which will be validated by Azure.
    use_subdomain = custom_domain_use_subdomain # (Optional) Should the Custom Domain Name be validated by using indirect CNAME validation?
  }

  # This block is optional with no minimum number of items and no maximum number of items
  customer_managed_key {
    key_vault_key_id          = customer_managed_key_key_vault_key_id          # (Required) The ID of the Key Vault Key, supplying a version-less key ID will enable auto-rotation of this key.
    user_assigned_identity_id = customer_managed_key_user_assigned_identity_id # (Required) The ID of a user assigned identity.
  }

  # This block is optional with no minimum number of items and no maximum number of items
  identity {
    identity_ids = identity_identity_ids # (Optional) Specifies a list of User Assigned Managed Identity IDs to be assigned to this Storage Account.
    type         = identity_type         # (Required) Specifies the type of Managed Service Identity that should be configured on this Storage Account. Possible values are SystemAssigned, UserAssigned, SystemAssigned, UserAssigned (to enable both).
  }

  # This block is optional with no minimum number of items and no maximum number of items
  immutability_policy {
    allow_protected_append_writes = immutability_policy_allow_protected_append_writes # (Required) When enabled, new blocks can be written to an append blob while maintaining immutability protection and compliance. Only new blocks can be added and any existing blocks cannot be modified or deleted.
    period_since_creation_in_days = immutability_policy_period_since_creation_in_days # (Required) The immutability period for the blobs in the container since the policy creation, in days.
    state                         = immutability_policy_state                         # (Required) Defines the mode of the policy. Disabled state disables the policy, Unlocked state allows increase and decrease of immutability retention time and also allows toggling allowProtectedAppendWrites property, Locked state only allows the increase of the immutability retention time. A policy can only be created in a Disabled or Unlocked state and can be toggled between the two states. Only a policy in an Unlocked state can transition to a Locked state which cannot be reverted.
  }

  # This block is optional with no minimum number of items and no maximum number of items
  network_rules {
    default_action = network_rules_default_action # (Required) Specifies the default action of allow or deny when no other rules match. Valid options are Deny or Allow.

    # This block is optional with no minimum number of items and a maximum of 1 items
    private_link_access {
      endpoint_resource_id = network_rules_private_link_access_endpoint_resource_id # (Required) The resource id of the resource access rule to be granted access.
    }
  }

  # This block is optional with no minimum number of items and no maximum number of items
  queue_properties {

    # This block is optional with no minimum number of items and a maximum of 1 items
    cors_rule {
      allowed_headers    = queue_properties_cors_rule_allowed_headers    # (Required) A list of headers that are allowed to be a part of the cross-origin request.
      allowed_methods    = queue_properties_cors_rule_allowed_methods    # (Required) A list of HTTP methods that are allowed to be executed by the origin. Valid options are
      allowed_origins    = queue_properties_cors_rule_allowed_origins    # (Required) A list of origin domains that will be allowed by CORS.
      exposed_headers    = queue_properties_cors_rule_exposed_headers    # (Required) A list of response headers that are exposed to CORS clients.
      max_age_in_seconds = queue_properties_cors_rule_max_age_in_seconds # (Required) The number of seconds the client should cache a preflight response.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    hour_metrics {
      enabled               = queue_properties_hour_metrics_enabled               # (Required) Indicates whether hour metrics are enabled for the Queue service.
      include_apis          = queue_properties_hour_metrics_include_apis          # (Optional) Indicates whether metrics should generate summary statistics for called API operations.
      retention_policy_days = queue_properties_hour_metrics_retention_policy_days # (Optional) Specifies the number of days that logs will be retained.
      version               = queue_properties_hour_metrics_version               # (Required) The version of storage analytics to configure.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    logging {
      delete                = queue_properties_logging_delete                # (Required) Indicates whether all delete requests should be logged.
      read                  = queue_properties_logging_read                  # (Required) Indicates whether all read requests should be logged.
      retention_policy_days = queue_properties_logging_retention_policy_days # (Optional) Specifies the number of days that logs will be retained.
      version               = queue_properties_logging_version               # (Required) The version of storage analytics to configure.
      write                 = queue_properties_logging_write                 # (Required) Indicates whether all write requests should be logged.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    minute_metrics {
      enabled               = queue_properties_minute_metrics_enabled               # (Required) Indicates whether minute metrics are enabled for the Queue service.
      include_apis          = queue_properties_minute_metrics_include_apis          # (Optional) Indicates whether metrics should generate summary statistics for called API operations.
      retention_policy_days = queue_properties_minute_metrics_retention_policy_days # (Optional) Specifies the number of days that logs will be retained.
      version               = queue_properties_minute_metrics_version               # (Required) The version of storage analytics to configure.
    }
  }

  # This block is optional with no minimum number of items and no maximum number of items
  routing {
    choice                      = routing_choice                      # (Optional) Specifies the kind of network routing opted by the user. Possible values are InternetRouting and MicrosoftRouting. Defaults to MicrosoftRouting.
    publish_internet_endpoints  = routing_publish_internet_endpoints  # (Optional) Should internet routing storage endpoints be published? Defaults to false.
    publish_microsoft_endpoints = routing_publish_microsoft_endpoints # (Optional) Should Microsoft routing storage endpoints be published? Defaults to false.
  }

  # This block is optional with no minimum number of items and no maximum number of items
  sas_policy {
    expiration_action = sas_policy_expiration_action # (Optional) The SAS expiration action. The only possible value is Log at this moment. Defaults to Log.
    expiration_period = sas_policy_expiration_period # (Required) The SAS expiration period in format of DD.HH:MM:SS.
  }

  # This block is optional with no minimum number of items and no maximum number of items
  share_properties {

    # This block is optional with no minimum number of items and a maximum of 1 items
    cors_rule {
      allowed_headers    = share_properties_cors_rule_allowed_headers    # (Required) A list of headers that are allowed to be a part of the cross-origin request.
      allowed_methods    = share_properties_cors_rule_allowed_methods    # (Required) A list of HTTP methods that are allowed to be executed by the origin. Valid options are
      allowed_origins    = share_properties_cors_rule_allowed_origins    # (Required) A list of origin domains that will be allowed by CORS.
      exposed_headers    = share_properties_cors_rule_exposed_headers    # (Required) A list of response headers that are exposed to CORS clients.
      max_age_in_seconds = share_properties_cors_rule_max_age_in_seconds # (Required) The number of seconds the client should cache a preflight response.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    retention_policy {
      days = share_properties_retention_policy_days # (Required) Specifies the number of days that the blob can be restored, between 1 and 365 days. This must be less than the days specified for delete_retention_policy.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    smb {
      authentication_types            = share_properties_smb_authentication_types            # (Optional) A set of SMB authentication methods. Possible values are NTLMv2, and Kerberos.
      channel_encryption_type         = share_properties_smb_channel_encryption_type         # (Optional) A set of SMB channel encryption. Possible values are AES-128-CCM, AES-128-GCM, and AES-256-GCM.
      kerberos_ticket_encryption_type = share_properties_smb_kerberos_ticket_encryption_type # (Optional) A set of Kerberos ticket encryption. Possible values are RC4-HMAC, and AES-256.
      multichannel_enabled            = share_properties_smb_multichannel_enabled            # (Optional) Indicates whether multichannel is enabled. Defaults to false. This is only supported on Premium storage accounts.
      versions                        = share_properties_smb_versions                        # (Optional) A set of SMB protocol versions. Possible values are SMB2.1, SMB3.0, and SMB3.1.1.
    }
  }

  # This block is optional with no minimum number of items and no maximum number of items
  static_website {
    error_404_document = static_website_error_404_document # (Optional) The absolute path to a custom webpage that should be used when a request is made which does not correspond to an existing file.
    index_document     = static_website_index_document     # (Optional) The webpage that Azure Storage serves for requests to the root of a website or any subfolder. For example, index.html. The value is case-sensitive.
  }

  # This block is optional with no minimum number of items and no maximum number of items
  timeouts {
    create = timeouts_create # (Defaults to 60 minutes) Used when creating the Storage Account.
    delete = timeouts_delete # (Defaults to 60 minutes) Used when deleting the Storage Account.
    read   = timeouts_read   # (Defaults to 5 minutes) Used when retrieving the Storage Account.
    update = timeouts_update # (Defaults to 60 minutes) Used when updating the Storage Account.
  }
}