# Terraform docs: https://github.com/hashicorp/terraform-provider-azurerm/blob/v3.45.0/website/docs/r/resource_group.html.markdown
# This resource creates an Azure resource group
resource "azurerm_resource_group" "main" {
  location = var.location               # The Azure Region where the Resource Group should exist. Changing this forces a new Resource Group to be created.
  name     = "rg-${var.app}-${var.env}" # The Name which should be used for this Resource Group. Changing this forces a new Resource Group to be created.
  tags     = var.tags                   # A mapping of tags which should be assigned to the Resource Group.
}

resource "azurerm_api_management" "main" {
  client_certificate_enabled    = var.client_certificate_enabled
  gateway_disabled              = var.gateway_disabled
  location                      = var.location
  min_api_version               = var.min_api_version
  name                          = var.name
  notification_sender_email     = var.notification_sender_email
  policy                        = var.policy
  public_ip_address_id          = var.public_ip_address_id
  public_network_access_enabled = var.public_network_access_enabled
  publisher_email               = var.publisher_email
  publisher_name                = var.publisher_name
  resource_group_name           = var.resource_group_name
  sku_name                      = var.sku_name
  tags                          = var.tags
  virtual_network_type          = var.virtual_network_type
  zones                         = var.zones

  # This block is optional allowing for 0 to N item(s)
  additional_location {
    capacity             = var.additional_location_capacity
    gateway_disabled     = var.additional_location_gateway_disabled
    location             = var.additional_location_location
    public_ip_address_id = var.additional_location_public_ip_address_id
    zones                = var.additional_location_zones

    # This block is optional allowing for 0 to 1 item(s)
    virtual_network_configuration {
      subnet_id = var.additional_location_virtual_network_configuration_subnet_id
    }
  }

  # This block is optional allowing for 0 to 10 item(s)
  certificate {
    certificate_password = var.certificate_certificate_password
    encoded_certificate  = var.certificate_encoded_certificate
    store_name           = var.certificate_store_name
  }

  # This block is optional allowing for 0 to 1 item(s)
  delegation {
    subscriptions_enabled     = var.delegation_subscriptions_enabled
    url                       = var.delegation_url
    user_registration_enabled = var.delegation_user_registration_enabled
    validation_key            = var.delegation_validation_key
  }

  # This block is optional allowing for 0 to 1 item(s)
  hostname_configuration {

    # This block is optional allowing for 0 to N item(s)
    developer_portal {
      certificate                     = var.hostname_configuration_developer_portal_certificate
      certificate_password            = var.hostname_configuration_developer_portal_certificate_password
      host_name                       = var.hostname_configuration_developer_portal_host_name
      key_vault_id                    = var.hostname_configuration_developer_portal_key_vault_id
      negotiate_client_certificate    = true
      ssl_keyvault_identity_client_id = var.hostname_configuration_developer_portal_ssl_keyvault_identity_client_id
    }

    # This block is optional allowing for 0 to N item(s)
    management {
      certificate                     = var.hostname_configuration_management_certificate
      certificate_password            = var.hostname_configuration_management_certificate_password
      host_name                       = var.hostname_configuration_management_host_name
      key_vault_id                    = var.hostname_configuration_management_key_vault_id
      negotiate_client_certificate    = var.hostname_configuration_management_negotiate_client_certificate
      ssl_keyvault_identity_client_id = var.hostname_configuration_management_ssl_keyvault_identity_client_id
    }

    # This block is optional allowing for 0 to N item(s)
    portal {
      certificate                     = var.hostname_configuration_portal_certificate
      certificate_password            = var.hostname_configuration_portal_certificate_password
      host_name                       = var.hostname_configuration_portal_host_name
      key_vault_id                    = var.hostname_configuration_portal_key_vault_id
      negotiate_client_certificate    = var.hostname_configuration_portal_negotiate_client_certificate
      ssl_keyvault_identity_client_id = var.hostname_configuration_portal_ssl_keyvault_identity_client_id
    }

    # This block is optional allowing for 0 to N item(s)
    proxy {
      certificate                     = var.hostname_configuration_proxy_certificate
      certificate_password            = var.hostname_configuration_proxy_certificate_password
      default_ssl_binding             = var.hostname_configuration_proxy_default_ssl_binding
      host_name                       = var.hostname_configuration_proxy_host_name
      key_vault_id                    = var.hostname_configuration_proxy_key_vault_id
      negotiate_client_certificate    = var.hostname_configuration_proxy_negotiate_client_certificate
      ssl_keyvault_identity_client_id = var.hostname_configuration_proxy_ssl_keyvault_identity_client_id
    }

    # This block is optional allowing for 0 to N item(s)
    scm {
      certificate                     = var.hostname_configuration_scm_certificate
      certificate_password            = var.hostname_configuration_scm_certificate_password
      host_name                       = var.hostname_configuration_scm_host_name
      key_vault_id                    = var.hostname_configuration_scm_key_vault_id
      negotiate_client_certificate    = var.hostname_configuration_scm_negotiate_client_certificate
      ssl_keyvault_identity_client_id = var.hostname_configuration_scm_ssl_keyvault_identity_client_id
    }
  }

  # This block is optional allowing for 0 to 1 item(s)
  identity {
    identity_ids = var.identity_identity_ids
    type         = var.identity_type
  }

  # This block is optional allowing for 0 to 1 item(s)
  protocols {
    enable_http2 = var.protocols_enable_http2
  }

  # This block is optional allowing for 0 to 1 item(s)
  security {
    enable_backend_ssl30                                = var.security_enable_backend_ssl30
    enable_backend_tls10                                = var.security_enable_backend_tls10
    enable_backend_tls11                                = var.security_enable_backend_tls11
    enable_frontend_ssl30                               = var.security_enable_frontend_ssl30
    enable_frontend_tls10                               = var.security_enable_frontend_tls10
    enable_frontend_tls11                               = var.security_enable_frontend_tls11
    tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled = var.security_tls_ecdhe_ecdsa_with_aes128_cbc_sha_ciphers_enabled
    tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled = var.security_tls_ecdhe_ecdsa_with_aes256_cbc_sha_ciphers_enabled
    tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled   = var.security_tls_ecdhe_rsa_with_aes128_cbc_sha_ciphers_enabled
    tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled   = var.security_tls_ecdhe_rsa_with_aes256_cbc_sha_ciphers_enabled
    tls_rsa_with_aes128_cbc_sha256_ciphers_enabled      = var.security_tls_rsa_with_aes128_cbc_sha256_ciphers_enabled
    tls_rsa_with_aes128_cbc_sha_ciphers_enabled         = var.security_tls_rsa_with_aes128_cbc_sha_ciphers_enabled
    tls_rsa_with_aes128_gcm_sha256_ciphers_enabled      = var.security_tls_rsa_with_aes128_gcm_sha256_ciphers_enabled
    tls_rsa_with_aes256_cbc_sha256_ciphers_enabled      = var.security_tls_rsa_with_aes256_cbc_sha256_ciphers_enabled
    tls_rsa_with_aes256_cbc_sha_ciphers_enabled         = var.security_tls_rsa_with_aes256_cbc_sha_ciphers_enabled
    tls_rsa_with_aes256_gcm_sha384_ciphers_enabled      = var.security_tls_rsa_with_aes256_gcm_sha384_ciphers_enabled
    triple_des_ciphers_enabled                          = var.security_triple_des_ciphers_enabled
  }

  # This block is optional allowing for 0 to 1 item(s)
  sign_in {
    enabled = var.sign_in_enabled
  }

  # This block is optional allowing for 0 to 1 item(s)
  sign_up {
    enabled = var.sign_up_enabled

    # This block is required allowing for 1 item(s)
    terms_of_service {
      consent_required = var.sign_up_terms_of_service_consent_required
      enabled          = var.sign_up_terms_of_service_enabled
      text             = var.sign_up_terms_of_service_text
    }
  }

  # This block is optional allowing for 0 to 1 item(s)
  tenant_access {
    enabled = var.tenant_access_enabled
  }

  # This block is optional allowing for 0 to N item(s)
  timeouts {
    create = var.timeouts_create
    delete = var.timeouts_delete
    read   = var.timeouts_read
    update = var.timeouts_update
  }

  # This block is optional allowing for 0 to 1 item(s)
  virtual_network_configuration {
    subnet_id = var.virtual_network_configuration_subnet_id
  }
}