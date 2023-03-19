resource "azurerm_resource_group" "main" {
  location = var.location
  name     = var.name
  tags     = var.tags
}

resource "azurerm_api_management" "main" {
  client_certificate_enabled    = var.client_certificate_enabled    # (Optional) Enforce a client certificate to be presented on each request to the gateway? This is only supported when SKU type is Consumption.
  gateway_disabled              = var.gateway_disabled              # (Optional) Disable the gateway in main region? This is only supported when additional_location is set.
  location                      = var.location                      # (Required) The Azure location where the API Management Service exists. Changing this forces a new resource to be created.
  min_api_version               = var.min_api_version               # (Optional) The version which the control plane API calls to API Management service are limited with version equal to or newer than.
  name                          = var.name                          # (Required) The name of the API Management Service. Changing this forces a new resource to be created.
  public_ip_address_id          = var.public_ip_address_id          # (Optional) ID of a standard SKU IPv4 Public IP.
  public_network_access_enabled = var.public_network_access_enabled # (Optional) Is public access to the service allowed?. Defaults to true
  publisher_email               = var.publisher_email               # (Required) The email of publisher/company.
  publisher_name                = var.publisher_name                # (Required) The name of publisher/company.
  resource_group_name           = var.resource_group_name           # (Required) The name of the Resource Group in which the API Management Service should be exist. Changing this forces a new resource to be created.
  sku_name                      = var.sku_name                      # (Required) sku_name is a string consisting of two parts separated by an underscore(_). The first part is the name, valid values include: Consumption, Developer, Basic, Standard and Premium. The second part is the capacity (e.g. the number of deployed units of the sku), which must be a positive integer (e.g. Developer_1).
  tags                          = var.tags                          # (Optional) A mapping of tags assigned to the resource.
  virtual_network_type          = var.virtual_network_type          # (Optional) The type of virtual network you want to use, valid values include: None, External, Internal.
  zones                         = var.zones                         # (Optional) Specifies a list of Availability Zones in which this API Management service should be located. Changing this forces a new API Management service to be created.

  # This block is optional with no minimum number of items and no maximum number of items
  additional_location {
    gateway_disabled     = additional_location_gateway_disabled     # (Optional) Disable the gateway in main region? This is only supported when additional_location is set.
    location             = additional_location_location             # (Required) The name of the Azure Region in which the API Management Service should be expanded to.
    public_ip_address_id = additional_location_public_ip_address_id # (Optional) ID of a standard SKU IPv4 Public IP.
    zones                = additional_location_zones                # (Optional) A list of availability zones. Changing this forces a new resource to be created.

    # This block is optional with no minimum number of items and no maximum number of items
    virtual_network_configuration {
      subnet_id = additional_location_virtual_network_configuration_subnet_id # (Required) The id of the subnet that will be used for the API Management.
    }
  }

  # This block is optional with no minimum number of items and no maximum number of items
  dynamic "certificate" {
    for_each = var.certificate
    content {
      certificate_password = certificate.value["certificate_password"] # (Optional) The password for the certificate.
      encoded_certificate  = certificate.value["encoded_certificate"]  # (Required) The Base64 Encoded PFX or Base64 Encoded X.509 Certificate.
      store_name           = certificate.value["store_name"]           # (Required) The name of the Certificate Store where this certificate should be stored. Possible values are CertificateAuthority and Root.
    }
  }

  # This block is optional with no minimum number of items and no maximum number of items
  delegation {
    subscriptions_enabled     = delegation_subscriptions_enabled     # (Optional) Should subscription requests be delegated to an external url? Defaults to false.
    url                       = delegation_url                       # (Optional) The delegation URL.
    user_registration_enabled = delegation_user_registration_enabled # (Optional) Should user registration requests be delegated to an external url? Defaults to false.
    validation_key            = delegation_validation_key            # (Optional) A base64-encoded validation key to validate, that a request is coming from Azure API Management.
  }

  # This block is optional with no minimum number of items and no maximum number of items
  hostname_configuration {

    # This block is optional with no minimum number of items and a maximum of 1 items
    developer_portal {
      certificate                     = hostname_configuration_developer_portal_certificate                     # (Optional) One or more (up to 10) certificate blocks as defined below.
      certificate_password            = hostname_configuration_developer_portal_certificate_password            # (Optional) The password associated with the certificate provided above.
      host_name                       = hostname_configuration_developer_portal_host_name                       # (Required) The Hostname to use for the Management API.
      key_vault_id                    = hostname_configuration_developer_portal_key_vault_id                    # (Optional) The ID of the Key Vault Secret containing the SSL Certificate, which must be should be of the type application/x-pkcs12.
      negotiate_client_certificate    = hostname_configuration_developer_portal_negotiate_client_certificate    # (Optional) Should Client Certificate Negotiation be enabled for this Hostname? Defaults to false.
      ssl_keyvault_identity_client_id = hostname_configuration_developer_portal_ssl_keyvault_identity_client_id # (Optional) System or User Assigned Managed identity clientId as generated by Azure AD, which has GET access to the keyVault containing the SSL certificate.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    management {
      certificate                     = hostname_configuration_management_certificate                     # (Optional) One or more (up to 10) certificate blocks as defined below.
      certificate_password            = hostname_configuration_management_certificate_password            # (Optional) The password for the certificate.
      host_name                       = hostname_configuration_management_host_name                       # (Required) The Hostname to use for the Management API.
      key_vault_id                    = hostname_configuration_management_key_vault_id                    # (Optional) The ID of the Key Vault Secret containing the SSL Certificate, which must be should be of the type application/x-pkcs12.
      negotiate_client_certificate    = hostname_configuration_management_negotiate_client_certificate    # (Optional) Should Client Certificate Negotiation be enabled for this Hostname? Defaults to false.
      ssl_keyvault_identity_client_id = hostname_configuration_management_ssl_keyvault_identity_client_id # (Optional) The Managed Identity Client ID to use to access the Key Vault. This Identity must be specified in the identity block to be used.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    portal {
      certificate                     = hostname_configuration_portal_certificate                     # (Optional) The Base64 Encoded Certificate.
      certificate_password            = hostname_configuration_portal_certificate_password            # (Optional) The password for the certificate.
      host_name                       = hostname_configuration_portal_host_name                       # (Required) The Hostname to use for the Management API.
      key_vault_id                    = hostname_configuration_portal_key_vault_id                    # (Optional) The ID of the Key Vault Secret containing the SSL Certificate, which must be should be of the type application/x-pkcs12.
      negotiate_client_certificate    = hostname_configuration_portal_negotiate_client_certificate    # (Optional) Should Client Certificate Negotiation be enabled for this Hostname? Defaults to false.
      ssl_keyvault_identity_client_id = hostname_configuration_portal_ssl_keyvault_identity_client_id # (Optional) The Managed Identity Client ID to use to access the Key Vault. This Identity must be specified in the identity block to be used.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    proxy {
      certificate                     = hostname_configuration_proxy_certificate                     # (Optional) One or more (up to 10) certificate blocks as defined below.
      certificate_password            = hostname_configuration_proxy_certificate_password            # (Optional) The password for the certificate.
      host_name                       = hostname_configuration_proxy_host_name                       # (Required) The Hostname to use for the Management API.
      key_vault_id                    = hostname_configuration_proxy_key_vault_id                    # (Optional) The ID of the Key Vault Secret containing the SSL Certificate, which must be should be of the type application/x-pkcs12.
      negotiate_client_certificate    = hostname_configuration_proxy_negotiate_client_certificate    # (Optional) Should Client Certificate Negotiation be enabled for this Hostname? Defaults to false.
      ssl_keyvault_identity_client_id = hostname_configuration_proxy_ssl_keyvault_identity_client_id # (Optional) The Managed Identity Client ID to use to access the Key Vault. This Identity must be specified in the identity block to be used.
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    scm {
      certificate                     = hostname_configuration_scm_certificate                     # (Optional) The Base64 Encoded Certificate.
      certificate_password            = hostname_configuration_scm_certificate_password            # (Optional) The password for the certificate.
      host_name                       = hostname_configuration_scm_host_name                       # (Required) The Hostname to use for the Management API.
      key_vault_id                    = hostname_configuration_scm_key_vault_id                    # (Optional) The ID of the Key Vault Secret containing the SSL Certificate, which must be should be of the type application/x-pkcs12.
      negotiate_client_certificate    = hostname_configuration_scm_negotiate_client_certificate    # (Optional) Should Client Certificate Negotiation be enabled for this Hostname? Defaults to false.
      ssl_keyvault_identity_client_id = hostname_configuration_scm_ssl_keyvault_identity_client_id # (Optional) The Managed Identity Client ID to use to access the Key Vault. This Identity must be specified in the identity block to be used.
    }
  }

  # This block is optional with no minimum number of items and no maximum number of items
  identity {
    identity_ids = identity_identity_ids # (Optional) A list of User Assigned Managed Identity IDs to be assigned to this API Management Service.
    type         = identity_type         # (Required) Specifies the type of Managed Service Identity that should be configured on this API Management Service. Possible values are SystemAssigned, UserAssigned, SystemAssigned, UserAssigned (to enable both).
  }

  # This block is optional with no minimum number of items and no maximum number of items
  protocols {
    enable_http2 = protocols_enable_http2 # (Optional) Should HTTP/2 be supported by the API Management Service? Defaults to false.
  }

  # This block is optional with no minimum number of items and no maximum number of items
  security {
    enable_backend_ssl30                                = security_enable_backend_ssl30                                # (Optional) Should SSL 3.0 be enabled on the backend of the gateway? Defaults to false.
    enable_backend_tls10                                = security_enable_backend_tls10                                # (Optional) Should TLS 1.0 be enabled on the backend of the gateway? Defaults to false.
    enable_backend_tls11                                = security_enable_backend_tls11                                # (Optional) Should TLS 1.1 be enabled on the backend of the gateway? Defaults to false.
    enable_frontend_ssl30                               = security_enable_frontend_ssl30                               # (Optional) Should SSL 3.0 be enabled on the frontend of the gateway? Defaults to false.
    enable_frontend_tls10                               = security_enable_frontend_tls10                               # (Optional) Should TLS 1.0 be enabled on the frontend of the gateway? Defaults to false.
    enable_frontend_tls11                               = security_enable_frontend_tls11                               # (Optional) Should TLS 1.1 be enabled on the frontend of the gateway? Defaults to false.
    tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled = security_tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled # (Optional) Should the TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA cipher be enabled? Defaults to false.
    tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled = security_tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled # (Optional) Should the TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA cipher be enabled? Defaults to false.
    tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled   = security_tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled   # (Optional) Should the TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA cipher be enabled? Defaults to false.
    tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled   = security_tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled   # (Optional) Should the TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA cipher be enabled? Defaults to false.
    tls_rsa_with_aes128_cbc_sha256_ciphers_enabled      = security_tls_rsa_with_aes128_cbc_sha256_ciphers_enabled      # (Optional) Should the TLS_RSA_WITH_AES_128_CBC_SHA256 cipher be enabled? Defaults to false.
    tls_rsa_with_aes128_cbc_sha_ciphers_enabled         = security_tls_rsa_with_aes128_cbc_sha_ciphers_enabled         # (Optional) Should the TLS_RSA_WITH_AES_128_CBC_SHA cipher be enabled? Defaults to false.
    tls_rsa_with_aes128_gcm_sha256_ciphers_enabled      = security_tls_rsa_with_aes128_gcm_sha256_ciphers_enabled      # (Optional) Should the TLS_RSA_WITH_AES_128_GCM_SHA256 cipher be enabled? Defaults to false.
    tls_rsa_with_aes256_cbc_sha256_ciphers_enabled      = security_tls_rsa_with_aes256_cbc_sha256_ciphers_enabled      # (Optional) Should the TLS_RSA_WITH_AES_256_CBC_SHA256 cipher be enabled? Defaults to false.
    tls_rsa_with_aes256_cbc_sha_ciphers_enabled         = security_tls_rsa_with_aes256_cbc_sha_ciphers_enabled         # (Optional) Should the TLS_RSA_WITH_AES_256_CBC_SHA cipher be enabled? Defaults to false.
    tls_rsa_with_aes256_gcm_sha384_ciphers_enabled      = security_tls_rsa_with_aes256_gcm_sha384_ciphers_enabled      # (Optional) Should the TLS_RSA_WITH_AES_256_GCM_SHA384 cipher be enabled? Defaults to false.
    triple_des_ciphers_enabled                          = security_triple_des_ciphers_enabled                          # (Optional) Should the TLS_RSA_WITH_3DES_EDE_CBC_SHA cipher be enabled for alL TLS versions (1.0, 1.1 and 1.2)?
  }

  # This block is optional with no minimum number of items and no maximum number of items
  sign_in {
    enabled = sign_in_enabled # (Required) Can users sign up on the development portal?
  }

  # This block is optional with no minimum number of items and no maximum number of items
  sign_up {
    enabled = sign_up_enabled # (Required) Can users sign up on the development portal?

    # This block is optional with no minimum number of items and a maximum of 1 items
    terms_of_service {
      consent_required = sign_up_terms_of_service_consent_required # (Required) Should the user be asked for consent during sign up?
      enabled          = sign_up_terms_of_service_enabled          # (Required) Should Terms of Service be displayed during sign up?.
      text             = sign_up_terms_of_service_text             # (Optional) The Terms of Service which users are required to agree to in order to sign up.
    }
  }

  # This block is optional with no minimum number of items and no maximum number of items
  tenant_access {
    enabled = tenant_access_enabled # (Required) Should the access to the management API be enabled?
  }

  # This block is optional with no minimum number of items and no maximum number of items
  timeouts {
    create = timeouts_create # (Defaults to 3 hours) Used when creating the API Management Service.
    delete = timeouts_delete # (Defaults to 3 hours) Used when deleting the API Management Service.
    read   = timeouts_read   # (Defaults to 5 minutes) Used when retrieving the API Management Service.
    update = timeouts_update # (Defaults to 3 hours) Used when updating the API Management Service.
  }

  # This block is optional with no minimum number of items and no maximum number of items
  virtual_network_configuration {
    subnet_id = virtual_network_configuration_subnet_id # (Required) The id of the subnet that will be used for the API Management.
  }
}