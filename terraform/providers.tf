# Terraform docs: https://github.com/hashicorp/terraform-provider-azurerm
provider "azurerm" {

  # This block is required with a minimum of 1 items and a maximum of 1 items
  features {

    # This block is optional with no minimum number of items and a maximum of 1 items
    api_management {
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    app_configuration {
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    application_insights {
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    cognitive_account {
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    key_vault {
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    log_analytics_workspace {
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    managed_disk {
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    network {
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    resource_group {
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    template_deployment {
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    virtual_machine {
    }

    # This block is optional with no minimum number of items and a maximum of 1 items
    virtual_machine_scale_set {
    }
  }
}