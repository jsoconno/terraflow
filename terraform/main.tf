resource "azurerm_resource_group" "main" {
  location = var.location
  name     = var.name
  tags     = var.tags

  # This block is optional
  timeouts {
    create = var.timeouts_create
    delete = var.timeouts_delete
    read   = var.timeouts_read
    update = var.timeouts_update
  }
}

resource "azurerm_windows_function_app" "main" {
  app_settings                       = var.app_settings
  builtin_logging_enabled            = var.builtin_logging_enabled
  client_certificate_enabled         = var.client_certificate_enabled
  client_certificate_exclusion_paths = var.client_certificate_exclusion_paths
  client_certificate_mode            = var.client_certificate_mode
  content_share_force_disabled       = var.content_share_force_disabled
  daily_memory_time_quota            = var.daily_memory_time_quota
  enabled                            = var.enabled
  functions_extension_version        = var.functions_extension_version
  location                           = var.location
  name                               = var.name
  resource_group_name                = var.resource_group_name
  service_plan_id                    = var.service_plan_id
  storage_account_access_key         = var.storage_account_access_key
  storage_account_name               = var.storage_account_name
  storage_key_vault_secret_id        = var.storage_key_vault_secret_id
  storage_uses_managed_identity      = var.storage_uses_managed_identity
  tags                               = var.tags
  virtual_network_subnet_id          = var.virtual_network_subnet_id

  # This block is optional
  auth_settings {
    additional_login_parameters   = var.auth_settings_additional_login_parameters
    enabled                       = var.auth_settings_enabled
    issuer                        = var.auth_settings_issuer
    token_refresh_extension_hours = var.auth_settings_token_refresh_extension_hours
    token_store_enabled           = var.auth_settings_token_store_enabled

    # This block is optional
    facebook {
      app_id                  = var.auth_settings_facebook_app_id
      app_secret              = var.auth_settings_facebook_app_secret
      app_secret_setting_name = var.auth_settings_facebook_app_secret_setting_name
      oauth_scopes            = var.auth_settings_facebook_oauth_scopes

    }

    # This block is optional
    github {
      client_id                  = var.auth_settings_github_client_id
      client_secret              = var.auth_settings_github_client_secret
      client_secret_setting_name = var.auth_settings_github_client_secret_setting_name
      oauth_scopes               = var.auth_settings_github_oauth_scopes

    }

    # This block is optional
    google {
      client_id                  = var.auth_settings_google_client_id
      client_secret              = var.auth_settings_google_client_secret
      client_secret_setting_name = var.auth_settings_google_client_secret_setting_name
      oauth_scopes               = var.auth_settings_google_oauth_scopes

    }

    # This block is optional
    microsoft {
      client_id                  = var.auth_settings_microsoft_client_id
      client_secret              = var.auth_settings_microsoft_client_secret
      client_secret_setting_name = var.auth_settings_microsoft_client_secret_setting_name
      oauth_scopes               = var.auth_settings_microsoft_oauth_scopes

    }

    # This block is optional
    twitter {
      consumer_key                 = var.auth_settings_twitter_consumer_key
      consumer_secret              = var.auth_settings_twitter_consumer_secret
      consumer_secret_setting_name = var.auth_settings_twitter_consumer_secret_setting_name

    }

  }

  # This block is optional
  backup {
    enabled             = var.backup_enabled
    name                = var.backup_name
    storage_account_url = var.backup_storage_account_url

    # This block is required
    schedule {
      frequency_interval       = var.backup_schedule_frequency_interval
      frequency_unit           = var.backup_schedule_frequency_unit
      keep_at_least_one_backup = var.backup_schedule_keep_at_least_one_backup
      retention_period_days    = var.backup_schedule_retention_period_days

    }

  }

  # This block is optional
  connection_string {
    name  = var.connection_string_name
    type  = var.connection_string_type
    value = var.connection_string_value

  }

  # This block is optional
  identity {
    type = var.identity_type

  }

  # This block is required
  site_config {
    api_definition_url                     = var.site_config_api_definition_url
    api_management_api_id                  = var.site_config_api_management_api_id
    app_command_line                       = var.site_config_app_command_line
    application_insights_connection_string = var.site_config_application_insights_connection_string
    application_insights_key               = var.site_config_application_insights_key
    ftps_state                             = var.site_config_ftps_state
    health_check_path                      = var.site_config_health_check_path
    http2_enabled                          = var.site_config_http2_enabled
    load_balancing_mode                    = var.site_config_load_balancing_mode
    managed_pipeline_mode                  = var.site_config_managed_pipeline_mode
    minimum_tls_version                    = var.site_config_minimum_tls_version
    remote_debugging_enabled               = var.site_config_remote_debugging_enabled
    runtime_scale_monitoring_enabled       = var.site_config_runtime_scale_monitoring_enabled
    scm_minimum_tls_version                = var.site_config_scm_minimum_tls_version
    scm_use_main_ip_restriction            = var.site_config_scm_use_main_ip_restriction
    use_32_bit_worker                      = var.site_config_use_32_bit_worker
    vnet_route_all_enabled                 = var.site_config_vnet_route_all_enabled
    websockets_enabled                     = var.site_config_websockets_enabled

    # This block is optional
    app_service_logs {
      disk_quota_mb         = var.site_config_app_service_logs_disk_quota_mb
      retention_period_days = var.site_config_app_service_logs_retention_period_days

    }

    # This block is optional
    application_stack {
      dotnet_version          = var.site_config_application_stack_dotnet_version
      java_version            = var.site_config_application_stack_java_version
      node_version            = var.site_config_application_stack_node_version
      powershell_core_version = var.site_config_application_stack_powershell_core_version

    }

    # This block is optional
    cors {
      allowed_origins     = var.site_config_cors_allowed_origins
      support_credentials = var.site_config_cors_support_credentials

    }

  }

  # This block is optional
  sticky_settings {
    app_setting_names       = var.sticky_settings_app_setting_names
    connection_string_names = var.sticky_settings_connection_string_names

  }

  # This block is optional
  storage_account {
    access_key   = var.storage_account_access_key
    account_name = var.storage_account_account_name
    mount_path   = var.storage_account_mount_path
    name         = var.storage_account_name
    share_name   = var.storage_account_share_name
    type         = var.storage_account_type

  }

  # This block is optional
  timeouts {
    create = var.timeouts_create
    delete = var.timeouts_delete
    read   = var.timeouts_read
    update = var.timeouts_update

  }
}