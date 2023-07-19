resource "azurerm_windows_virtual_machine" "main" {
  admin_password                = var.admin_password
  admin_username                = var.admin_username
  allow_extension_operations    = var.allow_extension_operations
  availability_set_id           = var.availability_set_id
  capacity_reservation_group_id = var.capacity_reservation_group_id
  computer_name                 = var.computer_name
  custom_data                   = var.custom_data
  dedicated_host_group_id       = var.dedicated_host_group_id
  dedicated_host_id             = var.dedicated_host_id
  enable_automatic_updates      = var.enable_automatic_updates
  encryption_at_host_enabled    = var.encryption_at_host_enabled
  eviction_policy               = var.eviction_policy
  extensions_time_budget        = var.extensions_time_budget
  hotpatching_enabled           = var.hotpatching_enabled
  license_type                  = var.license_type
  location                      = var.location
  max_bid_price                 = var.max_bid_price
  name                          = var.name
  network_interface_ids         = var.network_interface_ids
  patch_assessment_mode         = var.patch_assessment_mode
  patch_mode                    = var.patch_mode
  platform_fault_domain         = var.platform_fault_domain
  priority                      = var.priority
  provision_vm_agent            = var.provision_vm_agent
  proximity_placement_group_id  = var.proximity_placement_group_id
  resource_group_name           = var.resource_group_name
  secure_boot_enabled           = var.secure_boot_enabled
  size                          = var.size
  source_image_id               = var.source_image_id
  tags                          = var.tags
  timezone                      = var.timezone
  user_data                     = var.user_data
  virtual_machine_scale_set_id  = var.virtual_machine_scale_set_id
  vtpm_enabled                  = var.vtpm_enabled
  zone                          = var.zone

  # This block is optional allowing for 0 to 1 item(s)
  additional_capabilities {
    ultra_ssd_enabled = var.additional_capabilities_ultra_ssd_enabled
  }

  # This block is optional allowing for 0 to N item(s)
  additional_unattend_content {
    content = var.additional_unattend_content_content
    setting = var.additional_unattend_content_setting
  }

  # This block is optional allowing for 0 to 1 item(s)
  boot_diagnostics {
    storage_account_uri = var.boot_diagnostics_storage_account_uri
  }

  # This block is optional allowing for 0 to 100 item(s)
  gallery_application {
    configuration_blob_uri = var.gallery_application_configuration_blob_uri
    order                  = var.gallery_application_order
    tag                    = var.gallery_application_tag
    version_id             = var.gallery_application_version_id
  }

  # This block is optional allowing for 0 to 1 item(s)
  identity {
    identity_ids = var.identity_identity_ids
    type         = var.identity_type
  }

  # This block is required allowing for 1 item(s)
  os_disk {
    caching                          = var.os_disk_caching
    disk_encryption_set_id           = var.os_disk_disk_encryption_set_id
    disk_size_gb                     = var.os_disk_disk_size_gb
    name                             = var.os_disk_name
    secure_vm_disk_encryption_set_id = var.os_disk_secure_vm_disk_encryption_set_id
    security_encryption_type         = var.os_disk_security_encryption_type
    storage_account_type             = var.os_disk_storage_account_type
    write_accelerator_enabled        = var.os_disk_write_accelerator_enabled
  }

  # This block is optional allowing for 0 to 1 item(s)
  plan {
    name      = var.plan_name
    product   = var.plan_product
    publisher = var.plan_publisher
  }

  # This block is optional allowing for 0 to N item(s)
  secret {
    key_vault_id = var.secret_key_vault_id

    # This block is required allowing for 1 to N item(s)
    certificate {
      store = var.secret_certificate_store
      url   = var.secret_certificate_url
    }
  }

  # This block is optional allowing for 0 to 1 item(s)
  source_image_reference {
    offer     = var.source_image_reference_offer
    publisher = var.source_image_reference_publisher
    sku       = var.source_image_reference_sku
    version   = var.source_image_reference_version
  }

  # This block is optional allowing for 0 to 1 item(s)
  termination_notification {
    enabled = var.termination_notification_enabled
    timeout = var.termination_notification_timeout
  }

  # This block is optional allowing for 0 to N item(s)
  timeouts {
    create = var.timeouts_create
    delete = var.timeouts_delete
    read   = var.timeouts_read
    update = var.timeouts_update
  }

  # This block is optional allowing for 0 to N item(s)
  winrm_listener {
    certificate_url = var.winrm_listener_certificate_url
    protocol        = var.winrm_listener_protocol
  }
}