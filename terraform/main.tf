# Terraform docs: https://github.com/hashicorp/terraform-provider-azurerm/blob/main/website/docs/r/key_vault.html.markdown
resource "azurerm_key_vault" "main" {
  enable_rbac_authorization       = var.test_enable_rbac_authorization       # (Optional) Boolean flag to specify whether Azure Key Vault uses Role Based Access Control (RBAC) for authorization of data actions.
  enabled_for_deployment          = var.test_enabled_for_deployment          # (Optional) Boolean flag to specify whether Azure Virtual Machines are permitted to retrieve certificates stored as secrets from the key vault.
  enabled_for_disk_encryption     = var.test_enabled_for_disk_encryption     # (Optional) Boolean flag to specify whether Azure Disk Encryption is permitted to retrieve secrets from the vault and unwrap keys.
  enabled_for_template_deployment = var.test_enabled_for_template_deployment # (Optional) Boolean flag to specify whether Azure Resource Manager is permitted to retrieve secrets from the key vault.
  location                        = var.test_location                        # (Required) Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
  name                            = var.test_name                            # (Required) Specifies the name of the Key Vault. Changing this forces a new resource to be created. The name must be globally unique. If the vault is in a recoverable state then the vault will need to be purged before reusing the name.
  public_network_access_enabled   = var.test_public_network_access_enabled   # (Optional) Whether public network access is allowed for this Key Vault. Defaults to true.
  purge_protection_enabled        = var.test_purge_protection_enabled        # (Optional) Is Purge Protection enabled for this Key Vault?
  resource_group_name             = var.test_resource_group_name             # (Required) The name of the resource group in which to create the Key Vault. Changing this forces a new resource to be created.
  sku_name                        = var.test_sku_name                        # (Required) The Name of the SKU used for this Key Vault. Possible values are standard and premium.
  soft_delete_retention_days      = var.test_soft_delete_retention_days      # (Optional) The number of days that items should be retained for once soft-deleted. This value can be between 7 and 90 (the default) days.
  tags                            = var.test_tags                            # (Optional) A mapping of tags to assign to the resource.
  tenant_id                       = var.test_tenant_id                       # (Required) The Azure Active Directory tenant ID that should be used for authenticating requests to the key vault.

  # This block is optional with no minimum number of items and no maximum number of items
  contact {
    email = var.test_contact_email # (Required) E-mail address of the contact.
    name  = var.test_contact_name  # (Optional) Name of the contact.
    phone = var.test_contact_phone # (Optional) Phone number of the contact.
  }

  # This block is optional with no minimum number of items and a maximum of 1 items
  network_acls {
    bypass                     = var.test_network_acls_bypass                     # (Required) Specifies which traffic can bypass the network rules. Possible values are AzureServices and None.
    default_action             = var.test_network_acls_default_action             # (Required) The Default Action to use when no rules match from ip_rules / virtual_network_subnet_ids. Possible values are Allow and Deny.
    ip_rules                   = var.test_network_acls_ip_rules                   # (Optional) One or more IP Addresses, or CIDR Blocks which should be able to access the Key Vault.
    virtual_network_subnet_ids = var.test_network_acls_virtual_network_subnet_ids # (Optional) One or more Subnet IDs which should be able to access this Key Vault.
  }

  # This block is optional with no minimum number of items and no maximum number of items
  timeouts {
    create = var.test_timeouts_create # (Defaults to 30 minutes) Used when creating the Key Vault.
    delete = var.test_timeouts_delete # (Defaults to 30 minutes) Used when deleting the Key Vault.
    read   = var.test_timeouts_read   # (Defaults to 5 minutes) Used when retrieving the Key Vault.
    update = var.test_timeouts_update # (Defaults to 30 minutes) Used when updating the Key Vault.
  }
}

resource "azurerm_virtual_network" "my_virtual_network" {
  address_space           = var.address_space           # (Required) The address space that is used the virtual network. You can supply more than one address space.
  bgp_community           = var.bgp_community           # (Optional) The BGP community attribute in format <as-number>:<community-value>.
  dns_servers             = var.dns_servers             # (Optional) List of IP addresses of DNS servers
  edge_zone               = var.edge_zone               # (Optional) Specifies the Edge Zone within the Azure Region where this Virtual Network should exist. Changing this forces a new Virtual Network to be created.
  flow_timeout_in_minutes = var.flow_timeout_in_minutes # (Optional) The flow timeout in minutes for the Virtual Network, which is used to enable connection tracking for intra-VM flows. Possible values are between 4 and 30 minutes.
  guid                    = var.guid                    # The GUID of the virtual network.
  id                      = var.id                      # (Required) The ID of DDoS Protection Plan.
  location                = var.location                # (Required) The location/region where the virtual network is created. Changing this forces a new resource to be created.
  name                    = var.name                    # (Required) The name of the virtual network. Changing this forces a new resource to be created.
  resource_group_name     = var.resource_group_name     # (Required) The name of the resource group in which to create the virtual network. Changing this forces a new resource to be created.
  subnet                  = var.subnet                  # (Optional) Can be specified multiple times to define multiple subnets. Each subnet block supports fields documented below.
  tags                    = var.tags                    # (Optional) A mapping of tags to assign to the resource.

  # This block is optional
  ddos_protection_plan {
    enable = var.ddos_protection_plan_enable # (Required) Enable/disable DDoS Protection Plan on Virtual Network.
    id     = var.ddos_protection_plan_id     # (Required) The ID of DDoS Protection Plan.
  }

  # This block is optional
  timeouts {
    create = var.timeouts_create # (Defaults to 30 minutes) Used when creating the Virtual Network.
    delete = var.timeouts_delete # (Defaults to 30 minutes) Used when deleting the Virtual Network.
    read   = var.timeouts_read   # (Defaults to 5 minutes) Used when retrieving the Virtual Network.
    update = var.timeouts_update # (Defaults to 30 minutes) Used when updating the Virtual Network.
  }
}