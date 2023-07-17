resource "aws_s3_bucket" "main" {
  bucket = "this-bucket"
}

resource "azurerm_virtual_network" "main" {
  address_space           = var.address_space
  bgp_community           = var.bgp_community
  dns_servers             = var.dns_servers
  edge_zone               = var.edge_zone
  flow_timeout_in_minutes = var.flow_timeout_in_minutes
  guid                    = var.guid
  id                      = var.id
  location                = var.location
  name                    = var.name
  resource_group_name     = var.resource_group_name
  subnet                  = var.subnet
  tags                    = var.tags

  # This block is optional
  ddos_protection_plan {
    enable = var.ddos_protection_plan_enable
    id     = var.ddos_protection_plan_id
  }
}

resource "azurerm_windows_virtual_machine" "main" {
  admin_password                = var.admin_password                # (Required) The Password which should be used for the local-administrator on this Virtual Machine. Changing this forces a new resource to be created.
  admin_username                = var.admin_username                # (Required) The username of the local administrator used for the Virtual Machine. Changing this forces a new resource to be created.
  allow_extension_operations    = var.allow_extension_operations    # (Optional) Should Extension Operations be allowed on this Virtual Machine? Defaults to true.
  availability_set_id           = var.availability_set_id           # (Optional) Specifies the ID of the Availability Set in which the Virtual Machine should exist. Changing this forces a new resource to be created.
  capacity_reservation_group_id = var.capacity_reservation_group_id # (Optional) Specifies the ID of the Capacity Reservation Group which the Virtual Machine should be allocated to.
  computer_name                 = var.computer_name                 # (Optional) Specifies the Hostname which should be used for this Virtual Machine. If unspecified this defaults to the value for the name field. If the value of the name field is not a valid computer_name, then you must specify computer_name. Changing this forces a new resource to be created.
  custom_data                   = var.custom_data                   # (Optional) The Base64-Encoded Custom Data which should be used for this Virtual Machine. Changing this forces a new resource to be created.
  dedicated_host_group_id       = var.dedicated_host_group_id       # (Optional) The ID of a Dedicated Host Group that this Windows Virtual Machine should be run within. Conflicts with dedicated_host_id.
  dedicated_host_id             = var.dedicated_host_id             # (Optional) The ID of a Dedicated Host where this machine should be run on. Conflicts with dedicated_host_group_id.
  edge_zone                     = var.edge_zone                     # (Optional) Specifies the Edge Zone within the Azure Region where this Windows Virtual Machine should exist. Changing this forces a new Windows Virtual Machine to be created.
  enable_automatic_updates      = var.enable_automatic_updates      # (Optional) Specifies if Automatic Updates are Enabled for the Windows Virtual Machine. Changing this forces a new resource to be created. Defaults to true.
  encryption_at_host_enabled    = var.encryption_at_host_enabled    # (Optional) Should all of the disks (including the temp disk) attached to this Virtual Machine be encrypted by enabling Encryption at Host?
  eviction_policy               = var.eviction_policy               # (Optional) Specifies what should happen when the Virtual Machine is evicted for price reasons when using a Spot instance. Possible values are Deallocate and Delete. Changing this forces a new resource to be created.
  extensions_time_budget        = var.extensions_time_budget        # (Optional) Specifies the duration allocated for all extensions to start. The time duration should be between 15 minutes and 120 minutes (inclusive) and should be specified in ISO 8601 format. Defaults to 90 minutes (PT1H30M).
  hotpatching_enabled           = var.hotpatching_enabled           # (Optional) Should the VM be patched without requiring a reboot? Possible values are true or false. Defaults to false. For more information about hot patching please see the product documentation.
  license_type                  = var.license_type                  # (Optional) Specifies the type of on-premise license (also known as Azure Hybrid Use Benefit) which should be used for this Virtual Machine. Possible values are None, Windows_Client and Windows_Server.
  location                      = var.location                      # (Required) The Azure location where the Windows Virtual Machine should exist. Changing this forces a new resource to be created.
  max_bid_price                 = var.max_bid_price                 # (Optional) The maximum price you're willing to pay for this Virtual Machine, in US Dollars; which must be greater than the current spot price. If this bid price falls below the current spot price the Virtual Machine will be evicted using the eviction_policy. Defaults to -1, which means that the Virtual Machine should not be evicted for price reasons.
  name                          = var.name                          # (Required) The name of the Windows Virtual Machine. Changing this forces a new resource to be created.
  network_interface_ids         = var.network_interface_ids         # (Required). A list of Network Interface IDs which should be attached to this Virtual Machine. The first Network Interface ID in this list will be the Primary Network Interface on the Virtual Machine.
  patch_assessment_mode         = var.patch_assessment_mode         # (Optional) Specifies the mode of VM Guest Patching for the Virtual Machine. Possible values are AutomaticByPlatform or ImageDefault. Defaults to ImageDefault.
  patch_mode                    = var.patch_mode                    # (Optional) Specifies the mode of in-guest patching to this Windows Virtual Machine. Possible values are Manual, AutomaticByOS and AutomaticByPlatform. Defaults to AutomaticByOS. For more information on patch modes please see the product documentation.
  platform_fault_domain         = var.platform_fault_domain         # (Optional) Specifies the Platform Fault Domain in which this Windows Virtual Machine should be created. Defaults to -1, which means this will be automatically assigned to a fault domain that best maintains balance across the available fault domains. Changing this forces a new Windows Virtual Machine to be created.
  priority                      = var.priority                      # (Optional) Specifies the priority of this Virtual Machine. Possible values are Regular and Spot. Defaults to Regular. Changing this forces a new resource to be created.
  provision_vm_agent            = var.provision_vm_agent            # (Optional) Should the Azure VM Agent be provisioned on this Virtual Machine? Defaults to true. Changing this forces a new resource to be created.
  proximity_placement_group_id  = var.proximity_placement_group_id  # (Optional) The ID of the Proximity Placement Group which the Virtual Machine should be assigned to.
  resource_group_name           = var.resource_group_name           # (Required) The name of the Resource Group in which the Windows Virtual Machine should be exist. Changing this forces a new resource to be created.
  secure_boot_enabled           = var.secure_boot_enabled           # (Optional) Specifies if Secure Boot and Trusted Launch is enabled for the Virtual Machine. Changing this forces a new resource to be created.
  size                          = var.size                          # (Required) The SKU which should be used for this Virtual Machine, such as Standard_F2.
  source_image_id               = var.source_image_id               # (Optional) The ID of the Image which this Virtual Machine should be created from. Changing this forces a new resource to be created. Possible Image ID types include Image IDs, Shared Image IDs, Shared Image Version IDs, Community Gallery Image IDs, Community Gallery Image Version IDs, Shared Gallery Image IDs and Shared Gallery Image Version IDs.
  tags                          = var.tags                          # (Optional) A mapping of tags which should be assigned to this Virtual Machine.
  timezone                      = var.timezone                      # (Optional) Specifies the Time Zone which should be used by the Virtual Machine, the possible values are defined here. Changing this forces a new resource to be created.
  user_data                     = var.user_data                     # (Optional) The Base64-Encoded User Data which should be used for this Virtual Machine.
  virtual_machine_scale_set_id  = var.virtual_machine_scale_set_id  # (Optional) Specifies the Orchestrated Virtual Machine Scale Set that this Virtual Machine should be created within. Changing this forces a new resource to be created.
  vtpm_enabled                  = var.vtpm_enabled                  # (Optional) Specifies if vTPM (virtual Trusted Platform Module) and Trusted Launch is enabled for the Virtual Machine. Changing this forces a new resource to be created.
  zone                          = var.zone                          # * zones - (Optional) Specifies the Availability Zone in which this Windows Virtual Machine should be located. Changing this forces a new Windows Virtual Machine to be created.

  # This block is optional
  additional_capabilities {
    ultra_ssd_enabled = var.additional_capabilities_ultra_ssd_enabled # (Optional) Should the capacity to enable Data Disks of the UltraSSD_LRS storage account type be supported on this Virtual Machine? Defaults to false.
  }

  # This block is optional
  additional_unattend_content {
    content = var.additional_unattend_content_content # (Required) The XML formatted content that is added to the unattend.xml file for the specified path and component. Changing this forces a new resource to be created.
    setting = var.additional_unattend_content_setting # (Required) The name of the setting to which the content applies. Possible values are AutoLogon and FirstLogonCommands. Changing this forces a new resource to be created.
  }

  # This block is optional
  boot_diagnostics {
    storage_account_uri = var.boot_diagnostics_storage_account_uri # (Optional) The Primary/Secondary Endpoint for the Azure Storage Account which should be used to store Boot Diagnostics, including Console Output and Screenshots from the Hypervisor.
  }

  # This block is optional
  gallery_application {
    configuration_blob_uri = var.gallery_application_configuration_blob_uri # (Optional) Specifies the URI to an Azure Blob that will replace the default configuration for the package if provided.
    order                  = var.gallery_application_order                  # (Optional) Specifies the order in which the packages have to be installed. Possible values are between 0 and 2,147,483,647.
    tag                    = var.gallery_application_tag                    # (Optional) Specifies a passthrough value for more generic context. This field can be any valid string value.
    version_id             = var.gallery_application_version_id             # (Required) Specifies the Gallery Application Version resource ID.
  }

  # This block is optional
  identity {
    identity_ids = var.identity_identity_ids # (Optional) Specifies a list of User Assigned Managed Identity IDs to be assigned to this Windows Virtual Machine.
    type         = var.identity_type         # (Required) Specifies the type of Managed Service Identity that should be configured on this Windows Virtual Machine. Possible values are SystemAssigned, UserAssigned, SystemAssigned, UserAssigned (to enable both).
  }

  # This block is required
  os_disk {
    caching                          = var.os_disk_caching                          # (Required) The Type of Caching which should be used for the Internal OS Disk. Possible values are None, ReadOnly and ReadWrite.
    disk_encryption_set_id           = var.os_disk_disk_encryption_set_id           # (Optional) The ID of the Disk Encryption Set which should be used to Encrypt this OS Disk. Conflicts with secure_vm_disk_encryption_set_id.
    disk_size_gb                     = var.os_disk_disk_size_gb                     # (Optional) The Size of the Internal OS Disk in GB, if you wish to vary from the size used in the image this Virtual Machine is sourced from.
    name                             = var.os_disk_name                             # (Optional) The name which should be used for the Internal OS Disk. Changing this forces a new resource to be created.
    secure_vm_disk_encryption_set_id = var.os_disk_secure_vm_disk_encryption_set_id # (Optional) The ID of the Disk Encryption Set which should be used to Encrypt this OS Disk when the Virtual Machine is a Confidential VM. Conflicts with disk_encryption_set_id. Changing this forces a new resource to be created.
    security_encryption_type         = var.os_disk_security_encryption_type         # (Optional) Encryption Type when the Virtual Machine is a Confidential VM. Possible values are VMGuestStateOnly and DiskWithVMGuestState. Changing this forces a new resource to be created.
    storage_account_type             = var.os_disk_storage_account_type             # (Required) The Type of Storage Account which should back this the Internal OS Disk. Possible values are Standard_LRS, StandardSSD_LRS, Premium_LRS, StandardSSD_ZRS and Premium_ZRS. Changing this forces a new resource to be created.
    write_accelerator_enabled        = var.os_disk_write_accelerator_enabled        # (Optional) Should Write Accelerator be Enabled for this OS Disk? Defaults to false.

    # This block is optional
    diff_disk_settings {
      option    = var.os_disk_diff_disk_settings_option    # (Required) Specifies the Ephemeral Disk Settings for the OS Disk. At this time the only possible value is Local. Changing this forces a new resource to be created.
      placement = var.os_disk_diff_disk_settings_placement # (Optional) Specifies where to store the Ephemeral Disk. Possible values are CacheDisk and ResourceDisk. Defaults to CacheDisk. Changing this forces a new resource to be created.
    }
  }

  # This block is optional
  plan {
    name      = var.plan_name      # (Optional) The name which should be used for the Internal OS Disk. Changing this forces a new resource to be created.
    product   = var.plan_product   # (Required) Specifies the Product of the Marketplace Image this Virtual Machine should be created from. Changing this forces a new resource to be created.
    publisher = var.plan_publisher # (Required) Specifies the publisher of the image used to create the virtual machines. Changing this forces a new resource to be created.
  }

  # This block is optional
  secret {
    key_vault_id = var.secret_key_vault_id # (Required) The ID of the Key Vault from which all Secrets should be sourced.

    # This block is required
    certificate {
      store = var.secret_certificate_store # (Required) The certificate store on the Virtual Machine where the certificate should be added.
      url   = var.secret_certificate_url   # (Required) The Secret URL of a Key Vault Certificate.
    }
  }

  # This block is optional
  source_image_reference {
    offer     = var.source_image_reference_offer     # (Required) Specifies the offer of the image used to create the virtual machines. Changing this forces a new resource to be created.
    publisher = var.source_image_reference_publisher # (Required) Specifies the publisher of the image used to create the virtual machines. Changing this forces a new resource to be created.
    sku       = var.source_image_reference_sku       # (Required) Specifies the SKU of the image used to create the virtual machines. Changing this forces a new resource to be created.
    version   = var.source_image_reference_version   # (Required) Specifies the version of the image used to create the virtual machines. Changing this forces a new resource to be created.
  }

  # This block is optional
  termination_notification {
    enabled = var.termination_notification_enabled # (Required) Should the termination notification be enabled on this Virtual Machine?
    timeout = var.termination_notification_timeout # (Optional) Length of time (in minutes, between 5 and 15) a notification to be sent to the VM on the instance metadata server till the VM gets deleted. The time duration should be specified in ISO 8601 format. Defaults to PT5M.
  }

  # This block is optional
  winrm_listener {
    certificate_url = var.winrm_listener_certificate_url # (Optional) The Secret URL of a Key Vault Certificate, which must be specified when protocol is set to Https. Changing this forces a new resource to be created.
    protocol        = var.winrm_listener_protocol        # (Required) Specifies the protocol of listener. Possible values are Http or Https. Changing this forces a new resource to be created.
  }
}