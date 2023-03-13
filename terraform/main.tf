data "azurerm_resource_group" "main" {
  name = var.name
}

resource "resource_group" "main" {
  location = var.location
  name     = var.name
  tags     = var.tags

  # This block is optional and allows only one item.
  timeouts {
    create = var.timeouts_create
    delete = var.timeouts_delete
    read   = var.timeouts_read
    update = var.timeouts_update
  }
}

resource "linux_function_app" "main" {
  app_settings                       = var.app_settings
  builtin_logging_enabled            = var.builtin_logging_enabled
  client_certificate_enabled         = var.client_certificate_enabled
  client_certificate_exclusion_paths = var.client_certificate_exclusion_paths
  client_certificate_mode            = var.client_certificate_mode
  content_share_force_disabled       = var.content_share_force_disabled
  daily_memory_time_quota            = var.daily_memory_time_quota
  enabled                            = var.enabled
  functions_extension_version        = var.functions_extension_version
  https_only                         = var.https_only
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

  # This block is optional and allows only one item.
  auth_settings {
    additional_login_parameters   = var.auth_settings_additional_login_parameters
    enabled                       = var.auth_settings_enabled
    issuer                        = var.auth_settings_issuer
    token_refresh_extension_hours = var.auth_settings_token_refresh_extension_hours
    token_store_enabled           = var.auth_settings_token_store_enabled

    # This block is optional and allows only one item.
    facebook {
      app_id                  = var.auth_settings_facebook_app_id
      app_secret              = var.auth_settings_facebook_app_secret
      app_secret_setting_name = var.auth_settings_facebook_app_secret_setting_name
      oauth_scopes            = var.auth_settings_facebook_oauth_scopes
    }

    # This block is optional and allows only one item.
    github {
      client_id                  = var.auth_settings_github_client_id
      client_secret              = var.auth_settings_github_client_secret
      client_secret_setting_name = var.auth_settings_github_client_secret_setting_name
      oauth_scopes               = var.auth_settings_github_oauth_scopes
    }

    # This block is optional and allows only one item.
    google {
      client_id                  = var.auth_settings_google_client_id
      client_secret              = var.auth_settings_google_client_secret
      client_secret_setting_name = var.auth_settings_google_client_secret_setting_name
      oauth_scopes               = var.auth_settings_google_oauth_scopes
    }

    # This block is optional and allows only one item.
    microsoft {
      client_id                  = var.auth_settings_microsoft_client_id
      client_secret              = var.auth_settings_microsoft_client_secret
      client_secret_setting_name = var.auth_settings_microsoft_client_secret_setting_name
      oauth_scopes               = var.auth_settings_microsoft_oauth_scopes
    }

    # This block is optional and allows only one item.
    twitter {
      consumer_key                 = var.auth_settings_twitter_consumer_key
      consumer_secret              = var.auth_settings_twitter_consumer_secret
      consumer_secret_setting_name = var.auth_settings_twitter_consumer_secret_setting_name
    }
  }

  # This block is optional and allows only one item.
  auth_settings_v2 {
    auth_enabled                            = var.auth_settings_v2_auth_enabled
    config_file_path                        = var.auth_settings_v2_config_file_path
    default_provider                        = var.auth_settings_v2_default_provider
    excluded_paths                          = var.auth_settings_v2_excluded_paths
    forward_proxy_convention                = var.auth_settings_v2_forward_proxy_convention
    forward_proxy_custom_host_header_name   = var.auth_settings_v2_forward_proxy_custom_host_header_name
    forward_proxy_custom_scheme_header_name = var.auth_settings_v2_forward_proxy_custom_scheme_header_name
    http_route_api_prefix                   = var.auth_settings_v2_http_route_api_prefix
    require_authentication                  = var.auth_settings_v2_require_authentication
    require_https                           = var.auth_settings_v2_require_https
    runtime_version                         = var.auth_settings_v2_runtime_version
    unauthenticated_action                  = var.auth_settings_v2_unauthenticated_action

    # This block is optional and allows only one item.
    active_directory_v2 {
      allowed_applications                 = var.auth_settings_v2_active_directory_v2_allowed_applications
      allowed_audiences                    = var.auth_settings_v2_active_directory_v2_allowed_audiences
      allowed_groups                       = var.auth_settings_v2_active_directory_v2_allowed_groups
      allowed_identities                   = var.auth_settings_v2_active_directory_v2_allowed_identities
      client_id                            = var.auth_settings_v2_active_directory_v2_client_id
      client_secret_certificate_thumbprint = var.auth_settings_v2_active_directory_v2_client_secret_certificate_thumbprint
      client_secret_setting_name           = var.auth_settings_v2_active_directory_v2_client_secret_setting_name
      jwt_allowed_client_applications      = var.auth_settings_v2_active_directory_v2_jwt_allowed_client_applications
      jwt_allowed_groups                   = var.auth_settings_v2_active_directory_v2_jwt_allowed_groups
      login_parameters                     = var.auth_settings_v2_active_directory_v2_login_parameters
      tenant_auth_endpoint                 = var.auth_settings_v2_active_directory_v2_tenant_auth_endpoint
      www_authentication_disabled          = var.auth_settings_v2_active_directory_v2_www_authentication_disabled
    }

    # This block is optional and allows only one item.
    apple_v2 {
      client_id                  = var.auth_settings_v2_apple_v2_client_id
      client_secret_setting_name = var.auth_settings_v2_apple_v2_client_secret_setting_name
    }

    # This block is optional and allows only one item.
    azure_static_web_app_v2 {
      client_id = var.auth_settings_v2_azure_static_web_app_v2_client_id
    }

    # This block is optional and allows only one item.
    custom_oidc_v2 {
      client_id                     = var.auth_settings_v2_custom_oidc_v2_client_id
      name                          = var.auth_settings_v2_custom_oidc_v2_name
      name_claim_type               = var.auth_settings_v2_custom_oidc_v2_name_claim_type
      openid_configuration_endpoint = var.auth_settings_v2_custom_oidc_v2_openid_configuration_endpoint
      scopes                        = var.auth_settings_v2_custom_oidc_v2_scopes
    }

    # This block is optional and allows only one item.
    facebook_v2 {
      app_id                  = var.auth_settings_v2_facebook_v2_app_id
      app_secret_setting_name = var.auth_settings_v2_facebook_v2_app_secret_setting_name
      login_scopes            = var.auth_settings_v2_facebook_v2_login_scopes
    }

    # This block is optional and allows only one item.
    github_v2 {
      client_id                  = var.auth_settings_v2_github_v2_client_id
      client_secret_setting_name = var.auth_settings_v2_github_v2_client_secret_setting_name
      login_scopes               = var.auth_settings_v2_github_v2_login_scopes
    }

    # This block is optional and allows only one item.
    google_v2 {
      allowed_audiences          = var.auth_settings_v2_google_v2_allowed_audiences
      client_id                  = var.auth_settings_v2_google_v2_client_id
      client_secret_setting_name = var.auth_settings_v2_google_v2_client_secret_setting_name
      login_scopes               = var.auth_settings_v2_google_v2_login_scopes
    }

    # This block is required and allows only one item.
    login {
      allowed_external_redirect_urls    = var.auth_settings_v2_login_allowed_external_redirect_urls
      cookie_expiration_convention      = var.auth_settings_v2_login_cookie_expiration_convention
      cookie_expiration_time            = var.auth_settings_v2_login_cookie_expiration_time
      logout_endpoint                   = var.auth_settings_v2_login_logout_endpoint
      nonce_expiration_time             = var.auth_settings_v2_login_nonce_expiration_time
      preserve_url_fragments_for_logins = var.auth_settings_v2_login_preserve_url_fragments_for_logins
      token_refresh_extension_time      = var.auth_settings_v2_login_token_refresh_extension_time
      token_store_enabled               = var.auth_settings_v2_login_token_store_enabled
      token_store_path                  = var.auth_settings_v2_login_token_store_path
      token_store_sas_setting_name      = var.auth_settings_v2_login_token_store_sas_setting_name
      validate_nonce                    = var.auth_settings_v2_login_validate_nonce
    }

    # This block is optional and allows only one item.
    microsoft_v2 {
      allowed_audiences          = var.auth_settings_v2_microsoft_v2_allowed_audiences
      client_id                  = var.auth_settings_v2_microsoft_v2_client_id
      client_secret_setting_name = var.auth_settings_v2_microsoft_v2_client_secret_setting_name
      login_scopes               = var.auth_settings_v2_microsoft_v2_login_scopes
    }

    # This block is optional and allows only one item.
    twitter_v2 {
      consumer_key                 = var.auth_settings_v2_twitter_v2_consumer_key
      consumer_secret_setting_name = var.auth_settings_v2_twitter_v2_consumer_secret_setting_name
    }
  }

  # This block is optional and allows only one item.
  backup {
    enabled             = var.backup_enabled
    name                = var.backup_name
    storage_account_url = var.backup_storage_account_url

    # This block is required and allows only one item.
    schedule {
      frequency_interval       = var.backup_schedule_frequency_interval
      frequency_unit           = var.backup_schedule_frequency_unit
      keep_at_least_one_backup = var.backup_schedule_keep_at_least_one_backup
      retention_period_days    = var.backup_schedule_retention_period_days
    }
  }

  # This block is optional and allows only one item.
  connection_string {
    name  = var.connection_string_name
    type  = var.connection_string_type
    value = var.connection_string_value
  }

  # This block is optional and allows only one item.
  identity {
    identity_ids = var.identity_identity_ids
    type         = var.identity_type
  }

  # This block is required and allows only one item.
  site_config {
    api_definition_url                            = var.site_config_api_definition_url
    api_management_api_id                         = var.site_config_api_management_api_id
    app_command_line                              = var.site_config_app_command_line
    application_insights_connection_string        = var.site_config_application_insights_connection_string
    application_insights_key                      = var.site_config_application_insights_key
    container_registry_managed_identity_client_id = var.site_config_container_registry_managed_identity_client_id
    container_registry_use_managed_identity       = var.site_config_container_registry_use_managed_identity
    ftps_state                                    = var.site_config_ftps_state
    health_check_path                             = var.site_config_health_check_path
    http2_enabled                                 = var.site_config_http2_enabled
    load_balancing_mode                           = var.site_config_load_balancing_mode
    managed_pipeline_mode                         = var.site_config_managed_pipeline_mode
    minimum_tls_version                           = var.site_config_minimum_tls_version
    remote_debugging_enabled                      = var.site_config_remote_debugging_enabled
    runtime_scale_monitoring_enabled              = var.site_config_runtime_scale_monitoring_enabled
    scm_minimum_tls_version                       = var.site_config_scm_minimum_tls_version
    scm_use_main_ip_restriction                   = var.site_config_scm_use_main_ip_restriction
    use_32_bit_worker                             = var.site_config_use_32_bit_worker
    vnet_route_all_enabled                        = var.site_config_vnet_route_all_enabled
    websockets_enabled                            = var.site_config_websockets_enabled

    # This block is optional and allows only one item.
    app_service_logs {
      disk_quota_mb         = var.site_config_app_service_logs_disk_quota_mb
      retention_period_days = var.site_config_app_service_logs_retention_period_days
    }

    # This block is optional and allows only one item.
    application_stack {
      dotnet_version              = var.site_config_application_stack_dotnet_version
      java_version                = var.site_config_application_stack_java_version
      node_version                = var.site_config_application_stack_node_version
      powershell_core_version     = var.site_config_application_stack_powershell_core_version
      python_version              = var.site_config_application_stack_python_version
      use_custom_runtime          = var.site_config_application_stack_use_custom_runtime
      use_dotnet_isolated_runtime = var.site_config_application_stack_use_dotnet_isolated_runtime

      # This block is optional and allows only one item.
      docker {
        image_name        = var.site_config_application_stack_docker_image_name
        image_tag         = var.site_config_application_stack_docker_image_tag
        registry_password = var.site_config_application_stack_docker_registry_password
        registry_url      = var.site_config_application_stack_docker_registry_url
        registry_username = var.site_config_application_stack_docker_registry_username
      }
    }

    # This block is optional and allows only one item.
    cors {
      allowed_origins     = var.site_config_cors_allowed_origins
      support_credentials = var.site_config_cors_support_credentials
    }
  }

  # This block is optional and allows only one item.
  sticky_settings {
    app_setting_names       = var.sticky_settings_app_setting_names
    connection_string_names = var.sticky_settings_connection_string_names
  }

  # This block is optional and allows only one item.
  storage_account {
    access_key   = var.storage_account_access_key
    account_name = var.storage_account_account_name
    mount_path   = var.storage_account_mount_path
    name         = var.storage_account_name
    share_name   = var.storage_account_share_name
    type         = var.storage_account_type
  }

  # This block is optional and allows only one item.
  timeouts {
    create = var.timeouts_create
    delete = var.timeouts_delete
    read   = var.timeouts_read
    update = var.timeouts_update
  }
}