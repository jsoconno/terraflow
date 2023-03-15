resource "azurerm_resource_group" "main" {
  location = var.location # (Required) The Azure Region where the Resource Group should exist. Changing this forces a new Resource Group to be created.
  name     = var.name     # (Required) The Name which should be used for this Resource Group. Changing this forces a new Resource Group to be created.
  tags     = var.tags     # (Optional) A mapping of tags which should be assigned to the Resource Group.
}

resource "azurerm_linux_function_app" "main" {
  app_settings                       = var.app_settings                       # A map of key-value pairs for [App Settings](https://docs.microsoft.com/en-us/azure/azure-functions/functions-app-settings) and custom values.
  builtin_logging_enabled            = var.builtin_logging_enabled            # Should built in logging be enabled. Configures `AzureWebJobsDashboard` app setting based on the configured storage setting
  client_certificate_enabled         = var.client_certificate_enabled         # Should the function app use Client Certificates
  client_certificate_exclusion_paths = var.client_certificate_exclusion_paths # Paths to exclude when using client certificates, separated by ;
  client_certificate_mode            = var.client_certificate_mode            # The mode of the Function App's client certificates requirement for incoming requests. Possible values are `Required`, `Optional`, and `OptionalInteractiveUser` 
  content_share_force_disabled       = var.content_share_force_disabled       # Force disable the content share settings.
  daily_memory_time_quota            = var.daily_memory_time_quota            # The amount of memory in gigabyte-seconds that your application is allowed to consume per day. Setting this value only affects function apps in Consumption Plans.
  enabled                            = var.enabled                            # Is the Linux Function App enabled.
  functions_extension_version        = var.functions_extension_version        # The runtime version associated with the Function App.
  https_only                         = var.https_only                         # Can the Function App only be accessed via HTTPS?
  location                           = "eastus"                               # (Required) The Azure Region where the Linux Function App should exist. Changing this forces a new Linux Function App to be created.
  name                               = var.name                               # Specifies the name of the Function App.
  resource_group_name                = var.resource_group_name                # (Required) The name of the Resource Group where the Linux Function App should exist. Changing this forces a new Linux Function App to be created.
  service_plan_id                    = var.service_plan_id                    # The ID of the App Service Plan within which to create this Function App
  storage_account_access_key         = var.storage_account_access_key         # The access key which will be used to access the storage account for the Function App.
  storage_account_name               = var.storage_account_name               # The backend storage account name which will be used by this Function App.
  storage_key_vault_secret_id        = var.storage_key_vault_secret_id        # The Key Vault Secret ID, including version, that contains the Connection String to connect to the storage account for this Function App.
  storage_uses_managed_identity      = var.storage_uses_managed_identity      # Should the Function App use its Managed Identity to access storage?
  tags                               = var.tags                               # (Optional) A mapping of tags which should be assigned to the Linux Function App.
  virtual_network_subnet_id          = var.virtual_network_subnet_id

  # This block is optional with no minimum number of items and a maximum of 1 items
  auth_settings {
    additional_login_parameters   = var.auth_settings_additional_login_parameters   # Specifies a map of Login Parameters to send to the OpenID Connect authorization endpoint when a user logs in.
    enabled                       = var.auth_settings_enabled                       # Should the Authentication / Authorization feature be enabled?
    issuer                        = var.auth_settings_issuer                        # The OpenID Connect Issuer URI that represents the entity which issues access tokens.
    token_refresh_extension_hours = var.auth_settings_token_refresh_extension_hours # The number of hours after session token expiration that a session token can be used to call the token refresh API. Defaults to `72` hours.
    token_store_enabled           = var.auth_settings_token_store_enabled           # Should the Windows Web App durably store platform-specific security tokens that are obtained during login flows? Defaults to `false`.

    # This block is optional with no minimum number of items and a maximum of 1 items
    active_directory {
      allowed_audiences          = var.auth_settings_active_directory_allowed_audiences          # Specifies a list of Allowed audience values to consider when validating JWTs issued by Azure Active Directory.
      client_id                  = var.auth_settings_active_directory_client_id                  # The ID of the Client to use to authenticate with Azure Active Directory.
      client_secret              = var.auth_settings_active_directory_client_secret              # The Client Secret for the Client ID. Cannot be used with `client_secret_setting_name`.
      client_secret_setting_name = var.auth_settings_active_directory_client_secret_setting_name # The App Setting name that contains the client secret of the Client. Cannot be used with `client_secret`.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    facebook {
      app_id                  = var.auth_settings_facebook_app_id                  # The App ID of the Facebook app used for login.
      app_secret              = var.auth_settings_facebook_app_secret              # The App Secret of the Facebook app used for Facebook Login. Cannot be specified with `app_secret_setting_name`.
      app_secret_setting_name = var.auth_settings_facebook_app_secret_setting_name # The app setting name that contains the `app_secret` value used for Facebook Login. Cannot be specified with `app_secret`.
      oauth_scopes            = var.auth_settings_facebook_oauth_scopes            # Specifies a list of OAuth 2.0 scopes to be requested as part of Facebook Login authentication.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    github {
      client_id                  = var.auth_settings_github_client_id                  # The ID of the GitHub app used for login.
      client_secret              = var.auth_settings_github_client_secret              # The Client Secret of the GitHub app used for GitHub Login. Cannot be specified with `client_secret_setting_name`.
      client_secret_setting_name = var.auth_settings_github_client_secret_setting_name # The app setting name that contains the `client_secret` value used for GitHub Login. Cannot be specified with `client_secret`.
      oauth_scopes               = var.auth_settings_github_oauth_scopes               # Specifies a list of OAuth 2.0 scopes that will be requested as part of GitHub Login authentication.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    google {
      client_id                  = var.auth_settings_google_client_id                  # The OpenID Connect Client ID for the Google web application.
      client_secret              = var.auth_settings_google_client_secret              # The client secret associated with the Google web application.  Cannot be specified with `client_secret_setting_name`.
      client_secret_setting_name = var.auth_settings_google_client_secret_setting_name # The app setting name that contains the `client_secret` value used for Google Login. Cannot be specified with `client_secret`.
      oauth_scopes               = var.auth_settings_google_oauth_scopes               # Specifies a list of OAuth 2.0 scopes that will be requested as part of Google Sign-In authentication. If not specified, "openid", "profile", and "email" are used as default scopes.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    microsoft {
      client_id                  = var.auth_settings_microsoft_client_id                  # The OAuth 2.0 client ID that was created for the app used for authentication.
      client_secret              = var.auth_settings_microsoft_client_secret              # The OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with `client_secret_setting_name`.
      client_secret_setting_name = var.auth_settings_microsoft_client_secret_setting_name # The app setting name containing the OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with `client_secret`.
      oauth_scopes               = var.auth_settings_microsoft_oauth_scopes               # The list of OAuth 2.0 scopes that will be requested as part of Microsoft Account authentication. If not specified, `wl.basic` is used as the default scope.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    twitter {
      consumer_key                 = var.auth_settings_twitter_consumer_key                 # The OAuth 1.0a consumer key of the Twitter application used for sign-in.
      consumer_secret              = var.auth_settings_twitter_consumer_secret              # The OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with `consumer_secret_setting_name`.
      consumer_secret_setting_name = var.auth_settings_twitter_consumer_secret_setting_name # The app setting name that contains the OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with `consumer_secret`.
    }
  }

  # This block is optional with no minimum number of items and a maximum of 1 items
  auth_settings_v2 {
    auth_enabled                            = var.auth_settings_v2_auth_enabled                            # Should the AuthV2 Settings be enabled. Defaults to `false`
    config_file_path                        = var.auth_settings_v2_config_file_path                        # The path to the App Auth settings. **Note:** Relative Paths are evaluated from the Site Root directory.
    default_provider                        = var.auth_settings_v2_default_provider                        # The Default Authentication Provider to use when the `unauthenticated_action` is set to `RedirectToLoginPage`.
    excluded_paths                          = var.auth_settings_v2_excluded_paths                          # The paths which should be excluded from the `unauthenticated_action` when it is set to `RedirectToLoginPage`.
    forward_proxy_convention                = var.auth_settings_v2_forward_proxy_convention                # The convention used to determine the url of the request made. Possible values include `ForwardProxyConventionNoProxy`, `ForwardProxyConventionStandard`, `ForwardProxyConventionCustom`. Defaults to `ForwardProxyConventionNoProxy`
    forward_proxy_custom_host_header_name   = var.auth_settings_v2_forward_proxy_custom_host_header_name   # The name of the header containing the host of the request.
    forward_proxy_custom_scheme_header_name = var.auth_settings_v2_forward_proxy_custom_scheme_header_name # The name of the header containing the scheme of the request.
    http_route_api_prefix                   = var.auth_settings_v2_http_route_api_prefix                   # The prefix that should precede all the authentication and authorisation paths. Defaults to `/.auth`
    require_authentication                  = var.auth_settings_v2_require_authentication                  # Should the authentication flow be used for all requests.
    require_https                           = var.auth_settings_v2_require_https                           # Should HTTPS be required on connections? Defaults to true.
    runtime_version                         = var.auth_settings_v2_runtime_version                         # The Runtime Version of the Authentication and Authorisation feature of this App. Defaults to `~1`
    unauthenticated_action                  = var.auth_settings_v2_unauthenticated_action                  # The action to take for requests made without authentication. Possible values include `RedirectToLoginPage`, `AllowAnonymous`, `Return401`, and `Return403`. Defaults to `RedirectToLoginPage`.

    # This block is optional with no minimum number of items and a maximum of 1 items
    active_directory_v2 {
      allowed_applications                 = var.auth_settings_v2_active_directory_v2_allowed_applications                 # The list of allowed Applications for the Default Authorisation Policy.
      allowed_audiences                    = var.auth_settings_v2_active_directory_v2_allowed_audiences                    # Specifies a list of Allowed audience values to consider when validating JWTs issued by Azure Active Directory.
      allowed_groups                       = var.auth_settings_v2_active_directory_v2_allowed_groups                       # The list of allowed Group Names for the Default Authorisation Policy.
      allowed_identities                   = var.auth_settings_v2_active_directory_v2_allowed_identities                   # The list of allowed Identities for the Default Authorisation Policy.
      client_id                            = var.auth_settings_v2_active_directory_v2_client_id                            # The ID of the Client to use to authenticate with Azure Active Directory.
      client_secret_certificate_thumbprint = var.auth_settings_v2_active_directory_v2_client_secret_certificate_thumbprint # The thumbprint of the certificate used for signing purposes.
      client_secret_setting_name           = var.auth_settings_v2_active_directory_v2_client_secret_setting_name           # The App Setting name that contains the client secret of the Client.
      jwt_allowed_client_applications      = var.auth_settings_v2_active_directory_v2_jwt_allowed_client_applications      # A list of Allowed Client Applications in the JWT Claim.
      jwt_allowed_groups                   = var.auth_settings_v2_active_directory_v2_jwt_allowed_groups                   # A list of Allowed Groups in the JWT Claim.
      login_parameters                     = var.auth_settings_v2_active_directory_v2_login_parameters                     # A map of key-value pairs to send to the Authorisation Endpoint when a user logs in.
      tenant_auth_endpoint                 = var.auth_settings_v2_active_directory_v2_tenant_auth_endpoint                 # The Azure Tenant Endpoint for the Authenticating Tenant. e.g. `https://login.microsoftonline.com/v2.0/{tenant-guid}/`.
      www_authentication_disabled          = var.auth_settings_v2_active_directory_v2_www_authentication_disabled          # Should the www-authenticate provider should be omitted from the request? Defaults to `false`
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    apple_v2 {
      client_id                  = var.auth_settings_v2_apple_v2_client_id                  # The OpenID Connect Client ID for the Apple web application.
      client_secret_setting_name = var.auth_settings_v2_apple_v2_client_secret_setting_name # The app setting name that contains the `client_secret` value used for Apple Login.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    azure_static_web_app_v2 {
      client_id = var.auth_settings_v2_azure_static_web_app_v2_client_id # The ID of the Client to use to authenticate with Azure Static Web App Authentication.
    }

    # This block is optional with no minimum number of items and no maximum number of items
    custom_oidc_v2 {
      client_id                     = var.auth_settings_v2_custom_oidc_v2_client_id                     # The ID of the Client to use to authenticate with this Custom OIDC.
      name                          = var.auth_settings_v2_custom_oidc_v2_name                          # The name of the Custom OIDC Authentication Provider.
      name_claim_type               = var.auth_settings_v2_custom_oidc_v2_name_claim_type               # The name of the claim that contains the users name.
      openid_configuration_endpoint = var.auth_settings_v2_custom_oidc_v2_openid_configuration_endpoint # The endpoint that contains all the configuration endpoints for this Custom OIDC provider.
      scopes                        = var.auth_settings_v2_custom_oidc_v2_scopes                        # The list of the scopes that should be requested while authenticating.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    facebook_v2 {
      app_id                  = var.auth_settings_v2_facebook_v2_app_id                  # The App ID of the Facebook app used for login.
      app_secret_setting_name = var.auth_settings_v2_facebook_v2_app_secret_setting_name # The app setting name that contains the `app_secret` value used for Facebook Login.
      login_scopes            = var.auth_settings_v2_facebook_v2_login_scopes            # Specifies a list of scopes to be requested as part of Facebook Login authentication.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    github_v2 {
      client_id                  = var.auth_settings_v2_github_v2_client_id                  # The ID of the GitHub app used for login.
      client_secret_setting_name = var.auth_settings_v2_github_v2_client_secret_setting_name # The app setting name that contains the `client_secret` value used for GitHub Login.
      login_scopes               = var.auth_settings_v2_github_v2_login_scopes               # Specifies a list of OAuth 2.0 scopes that will be requested as part of GitHub Login authentication.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    google_v2 {
      allowed_audiences          = var.auth_settings_v2_google_v2_allowed_audiences          # Specifies a list of Allowed Audiences that will be requested as part of Google Sign-In authentication.
      client_id                  = var.auth_settings_v2_google_v2_client_id                  # The OpenID Connect Client ID for the Google web application.
      client_secret_setting_name = var.auth_settings_v2_google_v2_client_secret_setting_name # The app setting name that contains the `client_secret` value used for Google Login.
      login_scopes               = var.auth_settings_v2_google_v2_login_scopes               # Specifies a list of Login scopes that will be requested as part of Google Sign-In authentication.
    }

    # This block is required with a minimum of 1 items and a maximum of 1 items
    login {
      allowed_external_redirect_urls    = var.auth_settings_v2_login_allowed_external_redirect_urls    # External URLs that can be redirected to as part of logging in or logging out of the app. This is an advanced setting typically only needed by Windows Store application backends. **Note:** URLs within the current domain are always implicitly allowed.
      cookie_expiration_convention      = var.auth_settings_v2_login_cookie_expiration_convention      # The method by which cookies expire. Possible values include: `FixedTime`, and `IdentityProviderDerived`. Defaults to `FixedTime`.
      cookie_expiration_time            = var.auth_settings_v2_login_cookie_expiration_time            # The time after the request is made when the session cookie should expire. Defaults to `08:00:00`.
      logout_endpoint                   = var.auth_settings_v2_login_logout_endpoint                   # The endpoint to which logout requests should be made.
      nonce_expiration_time             = var.auth_settings_v2_login_nonce_expiration_time             # The time after the request is made when the nonce should expire. Defaults to `00:05:00`.
      preserve_url_fragments_for_logins = var.auth_settings_v2_login_preserve_url_fragments_for_logins # Should the fragments from the request be preserved after the login request is made. Defaults to `false`.
      token_refresh_extension_time      = var.auth_settings_v2_login_token_refresh_extension_time      # The number of hours after session token expiration that a session token can be used to call the token refresh API. Defaults to `72` hours.
      token_store_enabled               = var.auth_settings_v2_login_token_store_enabled               # Should the Token Store configuration Enabled. Defaults to `false`
      token_store_path                  = var.auth_settings_v2_login_token_store_path                  # The directory path in the App Filesystem in which the tokens will be stored.
      token_store_sas_setting_name      = var.auth_settings_v2_login_token_store_sas_setting_name      # The name of the app setting which contains the SAS URL of the blob storage containing the tokens.
      validate_nonce                    = var.auth_settings_v2_login_validate_nonce                    # Should the nonce be validated while completing the login flow. Defaults to `true`.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    microsoft_v2 {
      allowed_audiences          = var.auth_settings_v2_microsoft_v2_allowed_audiences          # Specifies a list of Allowed Audiences that will be requested as part of Microsoft Sign-In authentication.
      client_id                  = var.auth_settings_v2_microsoft_v2_client_id                  # The OAuth 2.0 client ID that was created for the app used for authentication.
      client_secret_setting_name = var.auth_settings_v2_microsoft_v2_client_secret_setting_name # The app setting name containing the OAuth 2.0 client secret that was created for the app used for authentication.
      login_scopes               = var.auth_settings_v2_microsoft_v2_login_scopes               # The list of Login scopes that will be requested as part of Microsoft Account authentication.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    twitter_v2 {
      consumer_key                 = var.auth_settings_v2_twitter_v2_consumer_key                 # The OAuth 1.0a consumer key of the Twitter application used for sign-in.
      consumer_secret_setting_name = var.auth_settings_v2_twitter_v2_consumer_secret_setting_name # The app setting name that contains the OAuth 1.0a consumer secret of the Twitter application used for sign-in.
    }
  }

  # This block is optional with no minimum number of items and a maximum of 1 items
  backup {
    enabled             = var.backup_enabled             # Should this backup job be enabled?
    name                = var.backup_name                # The name which should be used for this Backup.
    storage_account_url = var.backup_storage_account_url # The SAS URL to the container.

    # This block is required with a minimum of 1 items and a maximum of 1 items
    schedule {
      frequency_interval       = var.backup_schedule_frequency_interval       # How often the backup should be executed (e.g. for weekly backup, this should be set to `7` and `frequency_unit` should be set to `Day`).
      frequency_unit           = var.backup_schedule_frequency_unit           # The unit of time for how often the backup should take place. Possible values include: `Day` and `Hour`.
      keep_at_least_one_backup = var.backup_schedule_keep_at_least_one_backup # Should the service keep at least one backup, regardless of age of backup. Defaults to `false`.
      retention_period_days    = var.backup_schedule_retention_period_days    # After how many days backups should be deleted.
    }
  }

  # This block is optional with no minimum number of items and no maximum number of items
  connection_string {
    name  = var.connection_string_name  # The name which should be used for this Connection.
    type  = var.connection_string_type  # Type of database. Possible values include: `MySQL`, `SQLServer`, `SQLAzure`, `Custom`, `NotificationHub`, `ServiceBus`, `EventHub`, `APIHub`, `DocDb`, `RedisCache`, and `PostgreSQL`.
    value = var.connection_string_value # The connection string value.
  }

  # This block is optional with no minimum number of items and a maximum of 1 items
  identity {
    identity_ids = var.identity_identity_ids # (Optional) A list of User Assigned Managed Identity IDs to be assigned to this Linux Function App.
    type         = var.identity_type         # (Required) Specifies the type of Managed Service Identity that should be configured on this Linux Function App. Possible values are SystemAssigned, UserAssigned, SystemAssigned, UserAssigned (to enable both).
  }

  # This block is required with a minimum of 1 items and a maximum of 1 items
  site_config {
    api_definition_url                            = var.site_config_api_definition_url                            # The URL of the API definition that describes this Linux Function App.
    api_management_api_id                         = var.site_config_api_management_api_id                         # The ID of the API Management API for this Linux Function App.
    app_command_line                              = var.site_config_app_command_line                              # The program and any arguments used to launch this app via the command line. (Example `node myapp.js`).
    application_insights_connection_string        = var.site_config_application_insights_connection_string        # The Connection String for linking the Linux Function App to Application Insights.
    application_insights_key                      = var.site_config_application_insights_key                      # The Instrumentation Key for connecting the Linux Function App to Application Insights.
    container_registry_managed_identity_client_id = var.site_config_container_registry_managed_identity_client_id # The Client ID of the Managed Service Identity to use for connections to the Azure Container Registry.
    container_registry_use_managed_identity       = var.site_config_container_registry_use_managed_identity       # Should connections for Azure Container Registry use Managed Identity.
    ftps_state                                    = var.site_config_ftps_state                                    # State of FTP / FTPS service for this function app. Possible values include: `AllAllowed`, `FtpsOnly` and `Disabled`. Defaults to `Disabled`.
    health_check_path                             = var.site_config_health_check_path                             # The path to be checked for this function app health.
    http2_enabled                                 = var.site_config_http2_enabled                                 # Specifies if the http2 protocol should be enabled. Defaults to `false`.
    load_balancing_mode                           = var.site_config_load_balancing_mode                           # The Site load balancing mode. Possible values include: `WeightedRoundRobin`, `LeastRequests`, `LeastResponseTime`, `WeightedTotalTraffic`, `RequestHash`, `PerSiteRoundRobin`. Defaults to `LeastRequests` if omitted.
    managed_pipeline_mode                         = var.site_config_managed_pipeline_mode                         # The Managed Pipeline mode. Possible values include: `Integrated`, `Classic`. Defaults to `Integrated`.
    minimum_tls_version                           = var.site_config_minimum_tls_version                           # The configures the minimum version of TLS required for SSL requests. Possible values include: `1.0`, `1.1`, and  `1.2`. Defaults to `1.2`.
    remote_debugging_enabled                      = var.site_config_remote_debugging_enabled                      # Should Remote Debugging be enabled. Defaults to `false`.
    runtime_scale_monitoring_enabled              = var.site_config_runtime_scale_monitoring_enabled              # Should Functions Runtime Scale Monitoring be enabled.
    scm_minimum_tls_version                       = var.site_config_scm_minimum_tls_version                       # Configures the minimum version of TLS required for SSL requests to the SCM site Possible values include: `1.0`, `1.1`, and  `1.2`. Defaults to `1.2`.
    scm_use_main_ip_restriction                   = var.site_config_scm_use_main_ip_restriction                   # Should the Linux Function App `ip_restriction` configuration be used for the SCM also.
    use_32_bit_worker                             = var.site_config_use_32_bit_worker                             # Should the Linux Web App use a 32-bit worker.
    vnet_route_all_enabled                        = var.site_config_vnet_route_all_enabled                        # Should all outbound traffic to have Virtual Network Security Groups and User Defined Routes applied? Defaults to `false`.
    websockets_enabled                            = var.site_config_websockets_enabled                            # Should Web Sockets be enabled. Defaults to `false`.

    # This block is optional with no minimum number of items and a maximum of 1 items
    app_service_logs {
      disk_quota_mb         = var.site_config_app_service_logs_disk_quota_mb         # The amount of disk space to use for logs. Valid values are between `25` and `100`.
      retention_period_days = var.site_config_app_service_logs_retention_period_days # The retention period for logs in days. Valid values are between `0` and `99999`. Defaults to `0` (never delete).
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    application_stack {
      dotnet_version              = var.site_config_application_stack_dotnet_version              # The version of .Net. Possible values are `3.1`, `6.0` and `7.0`
      java_version                = var.site_config_application_stack_java_version                # The version of Java to use. Possible values are `8`, `11`, and `17`
      node_version                = var.site_config_application_stack_node_version                # The version of Node to use. Possible values include `12`, `14`, `16` and `18`
      powershell_core_version     = var.site_config_application_stack_powershell_core_version     # The version of PowerShell Core to use. Possibles values are `7`, and `7.2`
      python_version              = var.site_config_application_stack_python_version              # The version of Python to use. Possible values include `3.10`, `3.9`, `3.8`, and `3.7`.
      use_custom_runtime          = var.site_config_application_stack_use_custom_runtime          # (Optional) Should the Linux Function App use a custom runtime?
      use_dotnet_isolated_runtime = var.site_config_application_stack_use_dotnet_isolated_runtime # Should the DotNet process use an isolated runtime. Defaults to `false`.

      # This block is optional with no minimum number of items and no maximum number of items
      docker {
        image_name        = var.site_config_application_stack_docker_image_name        # The name of the Docker image to use.
        image_tag         = var.site_config_application_stack_docker_image_tag         # The image tag of the image to use.
        registry_password = var.site_config_application_stack_docker_registry_password # The password for the account to use to connect to the registry.
        registry_url      = var.site_config_application_stack_docker_registry_url      # The URL of the docker registry.
        registry_username = var.site_config_application_stack_docker_registry_username # The username to use for connections to the registry.
      }
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    cors {
      allowed_origins     = var.site_config_cors_allowed_origins     # Specifies a list of origins that should be allowed to make cross-origin calls.
      support_credentials = var.site_config_cors_support_credentials # Are credentials allowed in CORS requests? Defaults to `false`.
    }
  }

  # This block is optional with no minimum number of items and a maximum of 1 items
  sticky_settings {
    app_setting_names       = var.sticky_settings_app_setting_names       # (Optional) A list of app_setting names that the Linux Function App will not swap between Slots when a swap operation is triggered.
    connection_string_names = var.sticky_settings_connection_string_names # (Optional) A list of connection_string names that the Linux Function App will not swap between Slots when a swap operation is triggered.
  }

  # This block is optional with no minimum number of items and no maximum number of items
  storage_account {
    access_key   = var.storage_account_access_key   # (Required) The Access key for the storage account.
    account_name = var.storage_account_account_name # (Required) The Name of the Storage Account.
    mount_path   = var.storage_account_mount_path   # (Optional) The path at which to mount the storage share.
    name         = var.storage_account_name         # (Required) The name which should be used for this Storage Account.
    share_name   = var.storage_account_share_name   # (Required) The Name of the File Share or Container Name for Blob storage.
    type         = var.storage_account_type         # (Required) The Azure Storage Type. Possible values include AzureFiles and AzureBlob.
  }
}