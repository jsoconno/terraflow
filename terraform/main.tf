resource "azurerm_storage_account" "main" {
  account_kind                      = var.account_kind
  account_replication_type          = var.account_replication_type
  allow_nested_items_to_be_public   = var.allow_nested_items_to_be_public
  allowed_copy_scope                = var.allowed_copy_scope
  cross_tenant_replication_enabled  = var.cross_tenant_replication_enabled
  default_to_oauth_authentication   = var.default_to_oauth_authentication
  edge_zone                         = var.edge_zone
  enable_https_traffic_only         = var.enable_https_traffic_only
  infrastructure_encryption_enabled = var.infrastructure_encryption_enabled
  is_hns_enabled                    = var.is_hns_enabled
  location                          = var.location
  min_tls_version                   = var.min_tls_version
  name                              = var.name
  nfsv3_enabled                     = var.nfsv3_enabled
  public_network_access_enabled     = var.public_network_access_enabled
  queue_encryption_key_type         = var.queue_encryption_key_type
  resource_group_name               = var.resource_group_name
  sftp_enabled                      = var.sftp_enabled
  shared_access_key_enabled         = var.shared_access_key_enabled
  table_encryption_key_type         = var.table_encryption_key_type
  tags                              = var.tags

  # This block is optional with no minimum number of items and no maximum number of items
  dynamic "azure_files_authentication" {
    for_each = var.azure_files_authentication
    content {
      directory_type = azure_files_authentication.value["directory_type"]

      # This block is optional with no minimum number of items and a maximum of 1 items
      active_directory {
        domain_guid         = azure_files_authentication.value["active_directory_domain_guid"]
        domain_name         = azure_files_authentication.value["active_directory_domain_name"]
        domain_sid          = azure_files_authentication.value["active_directory_domain_sid"]
        forest_name         = azure_files_authentication.value["active_directory_forest_name"]
        netbios_domain_name = azure_files_authentication.value["active_directory_netbios_domain_name"]
        storage_sid         = azure_files_authentication.value["active_directory_storage_sid"]
      }
    }
  }

  # This block is optional with no minimum number of items and no maximum number of items
  blob_properties {
    change_feed_enabled           = blob_properties_change_feed_enabled
    change_feed_retention_in_days = blob_properties_change_feed_retention_in_days
    last_access_time_enabled      = blob_properties_last_access_time_enabled
    versioning_enabled            = blob_properties_versioning_enabled

    # This block is optional with no minimum number of items and a maximum of 1 items
    container_delete_retention_policy {
      days = blob_properties_container_delete_retention_policy_days
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    cors_rule {
      allowed_headers    = blob_properties_cors_rule_allowed_headers
      allowed_methods    = blob_properties_cors_rule_allowed_methods
      allowed_origins    = blob_properties_cors_rule_allowed_origins
      exposed_headers    = blob_properties_cors_rule_exposed_headers
      max_age_in_seconds = blob_properties_cors_rule_max_age_in_seconds
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    delete_retention_policy {
      days = blob_properties_delete_retention_policy_days
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    restore_policy {
      days = blob_properties_restore_policy_days
    }
  }

  # This block is optional with no minimum number of items and no maximum number of items
  custom_domain {
    name          = custom_domain_name
    use_subdomain = custom_domain_use_subdomain
  }

  # This block is optional with no minimum number of items and no maximum number of items
  customer_managed_key {
    key_vault_key_id          = customer_managed_key_key_vault_key_id
    user_assigned_identity_id = customer_managed_key_user_assigned_identity_id
  }

  # This block is optional with no minimum number of items and no maximum number of items
  identity {
    identity_ids = identity_identity_ids
    type         = identity_type
  }

  # This block is optional with no minimum number of items and no maximum number of items
  immutability_policy {
    allow_protected_append_writes = immutability_policy_allow_protected_append_writes
    period_since_creation_in_days = immutability_policy_period_since_creation_in_days
    state                         = immutability_policy_state
  }

  # This block is optional with no minimum number of items and no maximum number of items
  network_rules {
    default_action = network_rules_default_action

    # This block is optional with no minimum number of items and a maximum of 1 items
    private_link_access {
      endpoint_resource_id = network_rules_private_link_access_endpoint_resource_id
    }
  }

  # This block is optional with no minimum number of items and no maximum number of items
  queue_properties {

    # This block is optional with no minimum number of items and a maximum of 1 items
    cors_rule {
      allowed_headers    = queue_properties_cors_rule_allowed_headers
      allowed_methods    = queue_properties_cors_rule_allowed_methods
      allowed_origins    = queue_properties_cors_rule_allowed_origins
      exposed_headers    = queue_properties_cors_rule_exposed_headers
      max_age_in_seconds = queue_properties_cors_rule_max_age_in_seconds
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    hour_metrics {
      enabled               = queue_properties_hour_metrics_enabled
      include_apis          = queue_properties_hour_metrics_include_apis
      retention_policy_days = queue_properties_hour_metrics_retention_policy_days
      version               = queue_properties_hour_metrics_version
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    logging {
      delete                = queue_properties_logging_delete
      read                  = queue_properties_logging_read
      retention_policy_days = queue_properties_logging_retention_policy_days
      version               = queue_properties_logging_version
      write                 = queue_properties_logging_write
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    minute_metrics {
      enabled               = queue_properties_minute_metrics_enabled
      include_apis          = queue_properties_minute_metrics_include_apis
      retention_policy_days = queue_properties_minute_metrics_retention_policy_days
      version               = queue_properties_minute_metrics_version
    }
  }

  # This block is optional with no minimum number of items and no maximum number of items
  routing {
    choice                      = routing_choice
    publish_internet_endpoints  = routing_publish_internet_endpoints
    publish_microsoft_endpoints = routing_publish_microsoft_endpoints
  }

  # This block is optional with no minimum number of items and no maximum number of items
  sas_policy {
    expiration_action = sas_policy_expiration_action
    expiration_period = sas_policy_expiration_period
  }

  # This block is optional with no minimum number of items and no maximum number of items
  share_properties {

    # This block is optional with no minimum number of items and a maximum of 1 items
    cors_rule {
      allowed_headers    = share_properties_cors_rule_allowed_headers
      allowed_methods    = share_properties_cors_rule_allowed_methods
      allowed_origins    = share_properties_cors_rule_allowed_origins
      exposed_headers    = share_properties_cors_rule_exposed_headers
      max_age_in_seconds = share_properties_cors_rule_max_age_in_seconds
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    retention_policy {
      days = share_properties_retention_policy_days
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    smb {
      authentication_types            = share_properties_smb_authentication_types
      channel_encryption_type         = share_properties_smb_channel_encryption_type
      kerberos_ticket_encryption_type = share_properties_smb_kerberos_ticket_encryption_type
      multichannel_enabled            = share_properties_smb_multichannel_enabled
      versions                        = share_properties_smb_versions
    }
  }

  # This block is optional with no minimum number of items and no maximum number of items
  static_website {
    error_404_document = static_website_error_404_document
    index_document     = static_website_index_document
  }
}