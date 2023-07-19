resource "azurerm_windows_function_app" "main" {

  # This block is optional allowing for 0 to 1 item(s)
  auth_settings {

    # This block is optional allowing for 0 to 1 item(s)
    active_directory {
    }

    # This block is optional allowing for 0 to 1 item(s)
    facebook {
    }

    # This block is optional allowing for 0 to 1 item(s)
    github {
    }

    # This block is optional allowing for 0 to 1 item(s)
    google {
    }

    # This block is optional allowing for 0 to 1 item(s)
    microsoft {
    }

    # This block is optional allowing for 0 to 1 item(s)
    twitter {
    }
  }

  # This block is optional allowing for 0 to 1 item(s)
  backup {

    # This block is required allowing for 1 item(s)
    schedule {
    }
  }

  # This block is optional allowing for 0 to N item(s)
  connection_string {
  }

  # This block is optional allowing for 0 to 1 item(s)
  identity {
  }

  # This block is required allowing for 1 item(s)
  site_config {

    # This block is optional allowing for 0 to 1 item(s)
    app_service_logs {
    }

    # This block is optional allowing for 0 to 1 item(s)
    application_stack {
    }

    # This block is optional allowing for 0 to 1 item(s)
    cors {
    }
  }

  # This block is optional allowing for 0 to 1 item(s)
  sticky_settings {
  }

  # This block is optional allowing for 0 to N item(s)
  storage_account {
  }
}