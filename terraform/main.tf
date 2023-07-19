resource "azurerm_windows_function_app" "main" {
  app_settings                       = var.app_settings                       # A map of key-value pairs for App Settings and custom values.
  builtin_logging_enabled            = var.builtin_logging_enabled            # Should built in logging be enabled. Configures `AzureWebJobsDashboard` app setting based on the configured storage setting. Defaults to `true`.
  client_certificate_enabled         = var.client_certificate_enabled         # Should the function app use Client Certificates.
  client_certificate_exclusion_paths = var.client_certificate_exclusion_paths # Paths to exclude when using client certificates, separated by ;
  client_certificate_mode            = var.client_certificate_mode            # The mode of the Function App's client certificates requirement for incoming requests. Possible values are `Required`, `Optional`, and `OptionalInteractiveUser`.
  content_share_force_disabled       = var.content_share_force_disabled       # Should Content Share Settings be disabled. Defaults to `false`.
  daily_memory_time_quota            = var.daily_memory_time_quota            # The amount of memory in gigabyte-seconds that your application is allowed to consume per day. Setting this value only affects function apps under the consumption plan. Defaults to `0`.
  enabled                            = var.enabled                            # Is the Function App enabled? Defaults to `true`.
  functions_extension_version        = var.functions_extension_version        # The runtime version associated with the Function App. Defaults to `~4`.
  https_only                         = var.https_only                         # Can the Function App only be accessed via HTTPS? Defaults to `false`.
  key_vault_reference_identity_id    = var.key_vault_reference_identity_id    # The User Assigned Identity ID used for accessing KeyVault secrets. The identity must be assigned to the application in the `identity` block. For more information see - Access vaults with a user-assigned identity
  location                           = var.location                           # The Azure Region where the Windows Function App should exist. Changing this forces a new Windows Function App to be created.
  name                               = var.name                               # The name which should be used for this Windows Function App. Changing this forces a new Windows Function App to be created. Limit the function name to 32 characters to avoid naming collisions. For more information about Function App naming rule and Host ID Collisions
  resource_group_name                = var.resource_group_name                # The name of the Resource Group where the Windows Function App should exist. Changing this forces a new Windows Function App to be created.
  service_plan_id                    = var.service_plan_id                    # The ID of the App Service Plan within which to create this Function App.
  storage_account_access_key         = var.storage_account_access_key         # The access key which will be used to access the backend storage account for the Function App. Conflicts with `storage_uses_managed_identity`.
  storage_account_name               = var.storage_account_name               # The backend storage account name which will be used by this Function App.
  storage_key_vault_secret_id        = var.storage_key_vault_secret_id        # The Key Vault Secret ID, optionally including version, that contains the Connection String to connect to the storage account for this Function App.
  storage_uses_managed_identity      = var.storage_uses_managed_identity      # Should the Function App use Managed Identity to access the storage account. Conflicts with `storage_account_access_key`.
  tags                               = var.tags                               # A mapping of tags which should be assigned to the Windows Function App.
  virtual_network_subnet_id          = var.virtual_network_subnet_id          # The subnet id which will be used by this Function App for regional virtual network integration.

  # This block is optional allowing for 0 to 1 item(s)
  auth_settings {
    additional_login_parameters    = var.auth_settings_additional_login_parameters    # Specifies a map of login Parameters to send to the OpenID Connect authorization endpoint when a user logs in.
    allowed_external_redirect_urls = var.auth_settings_allowed_external_redirect_urls # Specifies a list of External URLs that can be redirected to as part of logging in or logging out of the Windows Function App.
    default_provider               = var.auth_settings_default_provider               # The default authentication provider to use when multiple providers are configured. Possible values include: `AzureActiveDirectory`, `Facebook`, `Google`, `MicrosoftAccount`, `Twitter`, `Github`
    enabled                        = var.auth_settings_enabled                        # Is the Function App enabled? Defaults to `true`.
    issuer                         = var.auth_settings_issuer                         # The OpenID Connect Issuer URI that represents the entity which issues access tokens for this Windows Function App.
    runtime_version                = var.auth_settings_runtime_version                # The Runtime Version of the Authentication / Authorization feature in use for the Windows Function App.
    token_refresh_extension_hours  = var.auth_settings_token_refresh_extension_hours  # The number of hours after session token expiration that a session token can be used to call the token refresh API. Defaults to `72` hours.
    token_store_enabled            = var.auth_settings_token_store_enabled            # Should the Windows Function App durably store platform-specific security tokens that are obtained during login flows? Defaults to `false`.
    unauthenticated_client_action  = var.auth_settings_unauthenticated_client_action  # The action to take when an unauthenticated client attempts to access the app. Possible values include: `RedirectToLoginPage`, `AllowAnonymous`.

    # This block is optional allowing for 0 to 1 item(s)
    active_directory {
      allowed_audiences          = var.auth_settings_active_directory_allowed_audiences          # Specifies a list of Allowed audience values to consider when validating JWTs issued by Azure Active Directory.
      client_id                  = var.auth_settings_active_directory_client_id                  # The ID of the Client to use to authenticate with Azure Active Directory.
      client_secret              = var.auth_settings_active_directory_client_secret              # The Client Secret for the Client ID. Cannot be used with `client_secret_setting_name`.
      client_secret_setting_name = var.auth_settings_active_directory_client_secret_setting_name # The App Setting name that contains the client secret of the Client. Cannot be used with `client_secret`.
    }

    # This block is optional allowing for 0 to 1 item(s)
    facebook {
      app_id                  = var.auth_settings_facebook_app_id                  # The App ID of the Facebook app used for login.
      app_secret              = var.auth_settings_facebook_app_secret              # The App Secret of the Facebook app used for Facebook login. Cannot be specified with `app_secret_setting_name`.
      app_secret_setting_name = var.auth_settings_facebook_app_secret_setting_name # The app setting name that contains the `app_secret` value used for Facebook login. Cannot be specified with `app_secret`.
      oauth_scopes            = var.auth_settings_facebook_oauth_scopes            # Specifies a list of OAuth 2.0 scopes to be requested as part of Facebook login authentication.
    }

    # This block is optional allowing for 0 to 1 item(s)
    github {
      client_id                  = var.auth_settings_github_client_id                  # The ID of the GitHub app used for login.
      client_secret              = var.auth_settings_github_client_secret              # The Client Secret of the GitHub app used for GitHub login. Cannot be specified with `client_secret_setting_name`.
      client_secret_setting_name = var.auth_settings_github_client_secret_setting_name # The app setting name that contains the `client_secret` value used for GitHub login. Cannot be specified with `client_secret`.
      oauth_scopes               = var.auth_settings_github_oauth_scopes               # Specifies a list of OAuth 2.0 scopes that will be requested as part of GitHub login authentication.
    }

    # This block is optional allowing for 0 to 1 item(s)
    google {
      client_id                  = var.auth_settings_google_client_id                  # The OpenID Connect Client ID for the Google web application.
      client_secret              = var.auth_settings_google_client_secret              # The client secret associated with the Google web application. Cannot be specified with `client_secret_setting_name`.
      client_secret_setting_name = var.auth_settings_google_client_secret_setting_name # The app setting name that contains the `client_secret` value used for Google login. Cannot be specified with `client_secret`.
      oauth_scopes               = var.auth_settings_google_oauth_scopes               # Specifies a list of OAuth 2.0 scopes that will be requested as part of Google Sign-In authentication. If not specified, `openid`, `profile`, and `email` are used as default scopes.
    }

    # This block is optional allowing for 0 to 1 item(s)
    microsoft {
      client_id                  = var.auth_settings_microsoft_client_id                  # The OAuth 2.0 client ID that was created for the app used for authentication.
      client_secret              = var.auth_settings_microsoft_client_secret              # The Client Secret for the Client ID. Cannot be used with `client_secret_setting_name`.
      client_secret_setting_name = var.auth_settings_microsoft_client_secret_setting_name # The App Setting name that contains the client secret of the Client. Cannot be used with `client_secret`.
      oauth_scopes               = var.auth_settings_microsoft_oauth_scopes               # Specifies a list of OAuth 2.0 scopes that will be requested as part of Microsoft Account authentication. If not specified, `wl.basic` is used as the default scope.
    }

    # This block is optional allowing for 0 to 1 item(s)
    twitter {
      consumer_key                 = var.auth_settings_twitter_consumer_key                 # The OAuth 1.0a consumer key of the Twitter application used for sign-in.
      consumer_secret              = var.auth_settings_twitter_consumer_secret              # The OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with `consumer_secret_setting_name`.
      consumer_secret_setting_name = var.auth_settings_twitter_consumer_secret_setting_name # The app setting name that contains the OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with `consumer_secret`.
    }
  }

  # This block is optional allowing for 0 to 1 item(s)
  backup {
    enabled             = var.backup_enabled             # Should this backup job be enabled? Defaults to `true`.
    name                = var.backup_name                # The name which should be used for this Backup.
    storage_account_url = var.backup_storage_account_url # The SAS URL to the container.

    # This block is required allowing for 1 item(s)
    schedule {
      frequency_interval       = var.backup_schedule_frequency_interval       # How often the backup should be executed (e.g. for weekly backup, this should be set to `7` and `frequency_unit` should be set to `Day`).
      frequency_unit           = var.backup_schedule_frequency_unit           # The unit of time for how often the backup should take place. Possible values include: `Day` and `Hour`.
      keep_at_least_one_backup = var.backup_schedule_keep_at_least_one_backup # Should the service keep at least one backup, regardless of age of backup. Defaults to `false`.
      retention_period_days    = var.backup_schedule_retention_period_days    # After how many days backups should be deleted. Defaults to `30`.
      start_time               = var.backup_schedule_start_time               # When the schedule should start working in RFC-3339 format.
    }
  }

  # This block is optional allowing for 0 to N item(s)
  connection_string {
    name  = var.connection_string_name  # The Site Credentials Username used for publishing.
    type  = var.connection_string_type  # The Azure Storage Type. Possible values include `AzureFiles`.
    value = var.connection_string_value # The connection string value.
  }

  # This block is optional allowing for 0 to 1 item(s)
  identity {
    identity_ids = var.identity_identity_ids # A list of User Assigned Managed Identity IDs to be assigned to this Windows Function App.
    type         = var.identity_type         # Specifies the type of Managed Service Identity that should be configured on this Windows Function App. Possible values are `SystemAssigned`, `UserAssigned`, `SystemAssigned, UserAssigned` (to enable both).
  }

  # This block is required allowing for 1 item(s)
  site_config {
    always_on                              = var.site_config_always_on                              # If this Windows Function App is Always On enabled. Defaults to `false`.
    api_definition_url                     = var.site_config_api_definition_url                     # The URL of the API definition that describes this Windows Function App.
    api_management_api_id                  = var.site_config_api_management_api_id                  # The ID of the API Management API for this Windows Function App.
    app_command_line                       = var.site_config_app_command_line                       # The App command line to launch.
    app_scale_limit                        = var.site_config_app_scale_limit                        # The number of workers this function app can scale out to. Only applicable to apps on the Consumption and Premium plan.
    application_insights_connection_string = var.site_config_application_insights_connection_string # The Connection String for linking the Windows Function App to Application Insights.
    application_insights_key               = var.site_config_application_insights_key               # The Instrumentation Key for connecting the Windows Function App to Application Insights.
    default_documents                      = var.site_config_default_documents                      # Specifies a list of Default Documents for the Windows Function App.
    elastic_instance_minimum               = var.site_config_elastic_instance_minimum               # The number of minimum instances for this Windows Function App. Only affects apps on Elastic Premium plans.
    ftps_state                             = var.site_config_ftps_state                             # State of FTP / FTPS service for this Windows Function App. Possible values include: `AllAllowed`, `FtpsOnly` and `Disabled`. Defaults to `Disabled`.
    health_check_eviction_time_in_min      = var.site_config_health_check_eviction_time_in_min      # The amount of time in minutes that a node can be unhealthy before being removed from the load balancer. Possible values are between `2` and `10`. Only valid in conjunction with `health_check_path`.
    health_check_path                      = var.site_config_health_check_path                      # The path to be checked for this Windows Function App health.
    http2_enabled                          = var.site_config_http2_enabled                          # Specifies if the HTTP2 protocol should be enabled. Defaults to `false`.
    ip_restriction                         = var.site_config_ip_restriction                         # One or more `ip_restriction` blocks as defined above.
    load_balancing_mode                    = var.site_config_load_balancing_mode                    # The Site load balancing mode. Possible values include: `WeightedRoundRobin`, `LeastRequests`, `LeastResponseTime`, `WeightedTotalTraffic`, `RequestHash`, `PerSiteRoundRobin`. Defaults to `LeastRequests` if omitted.
    managed_pipeline_mode                  = var.site_config_managed_pipeline_mode                  # Managed pipeline mode. Possible values include: `Integrated`, `Classic`. Defaults to `Integrated`.
    minimum_tls_version                    = var.site_config_minimum_tls_version                    # Configures the minimum version of TLS required for SSL requests. Possible values include: `1.0`, `1.1`, and `1.2`. Defaults to `1.2`.
    pre_warmed_instance_count              = var.site_config_pre_warmed_instance_count              # The number of pre-warmed instances for this Windows Function App. Only affects apps on an Elastic Premium plan.
    remote_debugging_enabled               = var.site_config_remote_debugging_enabled               # Should Remote Debugging be enabled. Defaults to `false`.
    remote_debugging_version               = var.site_config_remote_debugging_version               # The Remote Debugging Version. Possible values include `VS2017`, `VS2019`, and `VS2022`.
    runtime_scale_monitoring_enabled       = var.site_config_runtime_scale_monitoring_enabled       # Should Scale Monitoring of the Functions Runtime be enabled?
    scm_ip_restriction                     = var.site_config_scm_ip_restriction                     # One or more `scm_ip_restriction` blocks as defined above.
    scm_minimum_tls_version                = var.site_config_scm_minimum_tls_version                # Configures the minimum version of TLS required for SSL requests to the SCM site. Possible values include: `1.0`, `1.1`, and `1.2`. Defaults to `1.2`.
    scm_use_main_ip_restriction            = var.site_config_scm_use_main_ip_restriction            # Should the Windows Function App `ip_restriction` configuration be used for the SCM also.
    use_32_bit_worker                      = var.site_config_use_32_bit_worker                      # Should the Windows Function App use a 32-bit worker process. Defaults to `true`.
    vnet_route_all_enabled                 = var.site_config_vnet_route_all_enabled                 # Should all outbound traffic to have NAT Gateways, Network Security Groups and User Defined Routes applied? Defaults to `false`.
    websockets_enabled                     = var.site_config_websockets_enabled                     # Should Web Sockets be enabled. Defaults to `false`.
    worker_count                           = var.site_config_worker_count                           # The number of Workers for this Windows Function App.

    # This block is optional allowing for 0 to 1 item(s)
    app_service_logs {
      disk_quota_mb         = var.site_config_app_service_logs_disk_quota_mb         # The amount of disk space to use for logs. Valid values are between `25` and `100`. Defaults to `35`.
      retention_period_days = var.site_config_app_service_logs_retention_period_days # After how many days backups should be deleted. Defaults to `30`.
    }

    # This block is optional allowing for 0 to 1 item(s)
    application_stack {
      dotnet_version              = var.site_config_application_stack_dotnet_version              # The version of .NET to use. Possible values include `v3.0`, `v4.0` `v6.0` and `v7.0`.
      java_version                = var.site_config_application_stack_java_version                # The Version of Java to use. Supported versions include `1.8`, `11` & `17` (In-Preview).
      node_version                = var.site_config_application_stack_node_version                # The version of Node to run. Possible values include `~12`, `~14`, `~16` and `~18`.
      powershell_core_version     = var.site_config_application_stack_powershell_core_version     # The version of PowerShell Core to run. Possible values are `7`, and `7.2`.
      use_custom_runtime          = var.site_config_application_stack_use_custom_runtime          # Should the Windows Function App use a custom runtime?
      use_dotnet_isolated_runtime = var.site_config_application_stack_use_dotnet_isolated_runtime # Should the DotNet process use an isolated runtime. Defaults to `false`.
    }

    # This block is optional allowing for 0 to 1 item(s)
    cors {
      allowed_origins     = var.site_config_cors_allowed_origins     # Specifies a list of origins that should be allowed to make cross-origin calls.
      support_credentials = var.site_config_cors_support_credentials # Are credentials allowed in CORS requests? Defaults to `false`.
    }
  }

  # This block is optional allowing for 0 to 1 item(s)
  sticky_settings {
    app_setting_names       = var.sticky_settings_app_setting_names       # A list of `app_setting` names that the Windows Function App will not swap between Slots when a swap operation is triggered.
    connection_string_names = var.sticky_settings_connection_string_names # A list of `connection_string` names that the Windows Function App will not swap between Slots when a swap operation is triggered.
  }

  # This block is optional allowing for 0 to N item(s)
  storage_account {
    access_key   = var.storage_account_access_key   # The Access key for the storage account.
    account_name = var.storage_account_account_name # The Name of the Storage Account.
    mount_path   = var.storage_account_mount_path   # The path at which to mount the storage share.
    name         = var.storage_account_name         # The name which should be used for this Storage Account.
    share_name   = var.storage_account_share_name   # The Name of the File Share or Container Name for Blob storage.
    type         = var.storage_account_type         # The Azure Storage Type. Possible values include `AzureFiles`.
  }
}