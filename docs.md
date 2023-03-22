# terraflow
Terraform is an open-source infrastructure as code tool that   allows developers to manage cloud resources through code.   Terraflow provides developers with a set of commands and features   that can help them create, test, and deploy Terraform code more efficiently.    With Terraflow, developers can easily create Terraform modules, templates,   and configurations using a simple and intuitive command line interface. They   can also quickly generate code snippets and boilerplate code, reducing the   amount of manual work required to create new Terraform resources. 
## Usage
```
terraflow [OPTIONS] COMMAND [ARGS]...
```
## Options
```
  --version  Show the version and exit.
  --help     Show this message and exit.
```
## Commands
```
  data-source  Manage Terraform data sources.
  docs         Manage documentation.
  provider     Manage Terraform providers.
  resource     Manage Terraform resources.
  schema       Work with schemas.
  workspace    Manage workspaces.
```
## CLI Help
```
Usage: terraflow [OPTIONS] COMMAND [ARGS]...

  Terraform is an open-source infrastructure as code tool that
  allows developers to manage cloud resources through code.
  Terraflow provides developers with a set of commands and features
  that can help them create, test, and deploy Terraform code more efficiently.

  With Terraflow, developers can easily create Terraform modules, templates,
  and configurations using a simple and intuitive command line interface. They
  can also quickly generate code snippets and boilerplate code, reducing the
  amount of manual work required to create new Terraform resources.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  data-source  Manage Terraform data sources.
  docs         Manage documentation.
  provider     Manage Terraform providers.
  resource     Manage Terraform resources.
  schema       Work with schemas.
  workspace    Manage workspaces.
```

# terraflow workspace
Manage workspaces. 
## Usage
```
terraflow workspace [OPTIONS] COMMAND [ARGS]...
```
## Options
```
  --help  Show this message and exit.
```
## Commands
```
  create  Create a workspace.
  delete  Delete a workspace.
  get     Get a workspace.
  list    List workspaces.
  set     Set a workspace.
```
## CLI Help
```
Usage: terraflow workspace [OPTIONS] COMMAND [ARGS]...

  Manage workspaces.

Options:
  --help  Show this message and exit.

Commands:
  create  Create a workspace.
  delete  Delete a workspace.
  get     Get a workspace.
  list    List workspaces.
  set     Set a workspace.
```

# terraflow workspace set
Set a workspace. 
## Usage
```
terraflow workspace set [OPTIONS]
```
## Options
```
  --help  Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow workspace set [OPTIONS]

  Set a workspace.

Options:
  --help  Show this message and exit.
```

# terraflow workspace get
Get a workspace. 
## Usage
```
terraflow workspace get [OPTIONS]
```
## Options
```
  --help  Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow workspace get [OPTIONS]

  Get a workspace.

Options:
  --help  Show this message and exit.
```

# terraflow workspace list
List workspaces. 
## Usage
```
terraflow workspace list [OPTIONS]
```
## Options
```
  --help  Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow workspace list [OPTIONS]

  List workspaces.

Options:
  --help  Show this message and exit.
```

# terraflow workspace create
Create a workspace. 
## Usage
```
terraflow workspace create [OPTIONS]
```
## Options
```
  --help  Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow workspace create [OPTIONS]

  Create a workspace.

Options:
  --help  Show this message and exit.
```

# terraflow workspace delete
Delete a workspace. 
## Usage
```
terraflow workspace delete [OPTIONS]
```
## Options
```
  --help  Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow workspace delete [OPTIONS]

  Delete a workspace.

Options:
  --help  Show this message and exit.
```

# terraflow schema
Work with schemas. 
## Usage
```
terraflow schema [OPTIONS] COMMAND [ARGS]...
```
## Options
```
  --help  Show this message and exit.
```
## Commands
```
  download  Download the schema for the Terraform configuration.
```
## CLI Help
```
Usage: terraflow schema [OPTIONS] COMMAND [ARGS]...

  Work with schemas.

Options:
  --help  Show this message and exit.

Commands:
  download  Download the schema for the Terraform configuration.
```

# terraflow schema download
Download the schema for the Terraform configuration. 
## Usage
```
terraflow schema download [OPTIONS]
```
## Options
```
  --refresh               Refresh the downloaded schema file.
  --schema-filename TEXT  The name of the Terraform schema to use locally.
  --help                  Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow schema download [OPTIONS]

  Download the schema for the Terraform configuration.

Options:
  --refresh               Refresh the downloaded schema file.
  --schema-filename TEXT  The name of the Terraform schema to use locally.
  --help                  Show this message and exit.
```

# terraflow resource
Manage Terraform resources. 
## Usage
```
terraflow resource [OPTIONS] COMMAND [ARGS]...
```
## Options
```
  --help  Show this message and exit.
```
## Commands
```
  create  Create a Terraform resource.
  delete  Delete a resource from the configuration.
  list    List available resources for a provider.
```
## CLI Help
```
Usage: terraflow resource [OPTIONS] COMMAND [ARGS]...

  Manage Terraform resources.

Options:
  --help  Show this message and exit.

Commands:
  create  Create a Terraform resource.
  delete  Delete a resource from the configuration.
  list    List available resources for a provider.
```

# terraflow resource list
List available resources for a provider. 
## Usage
```
terraflow resource list [OPTIONS]
```
## Options
```
  --provider TEXT   The name of the Terraform provider.  [required]
  --namespace TEXT  The namespace of the Terraform provider.  [required]
  --keyword TEXT    A keyword used to filter results.
  --help            Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow resource list [OPTIONS]

  List available resources for a provider.

Options:
  --provider TEXT   The name of the Terraform provider.  [required]
  --namespace TEXT  The namespace of the Terraform provider.  [required]
  --keyword TEXT    A keyword used to filter results.
  --help            Show this message and exit.
```

# terraflow resource create
Create a Terraform resource. 
## Usage
```
terraflow resource create [OPTIONS]
```
## Options
```
  --refresh                      Refresh the downloaded schema file.
  --schema-filename TEXT         The name of the Terraform schema to use
                                 locally.
  --terraform-filename TEXT      The name of the target Terraform file.
  --provider TEXT                The name of the Terraform provider.
                                 [required]
  --namespace TEXT               The namespace of the Terraform provider.
                                 [required]
  --name TEXT                    The name to give the Terraform resource in
                                 the configuration.  For example, 'main' or
                                 'this'.
  --resource TEXT                The name of the terraform provider resource.
                                 [required]
  --terraform-filename TEXT      The name of the target Terraform file.
  --attribute-value-prefix TEXT  A prefix to give to all variables in the
                                 resource configuration.  Useful for module
                                 development.
  --attribute-default TEXT       Default values for a given attributes in the
                                 format 'attribute=value'.
  --ignore-attribute TEXT        Attributes to ignore in the configuration.
  --dynamic-block TEXT           Blocks to make dynamic in the configuration.
  --ignore-block TEXT            Blocks to ignore in the configuration.
  --add-descriptions             Add descriptions inline with the code for all
                                 resource attributes.
  --required-blocks-only         Only include required blocks in the resource
                                 configuration.
  --required-attributes-only     Only include required attributes in the
                                 resource configuration.
  --help                         Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow resource create [OPTIONS]

  Create a Terraform resource.

Options:
  --refresh                      Refresh the downloaded schema file.
  --schema-filename TEXT         The name of the Terraform schema to use
                                 locally.
  --terraform-filename TEXT      The name of the target Terraform file.
  --provider TEXT                The name of the Terraform provider.
                                 [required]
  --namespace TEXT               The namespace of the Terraform provider.
                                 [required]
  --name TEXT                    The name to give the Terraform resource in
                                 the configuration.  For example, 'main' or
                                 'this'.
  --resource TEXT                The name of the terraform provider resource.
                                 [required]
  --terraform-filename TEXT      The name of the target Terraform file.
  --attribute-value-prefix TEXT  A prefix to give to all variables in the
                                 resource configuration.  Useful for module
                                 development.
  --attribute-default TEXT       Default values for a given attributes in the
                                 format 'attribute=value'.
  --ignore-attribute TEXT        Attributes to ignore in the configuration.
  --dynamic-block TEXT           Blocks to make dynamic in the configuration.
  --ignore-block TEXT            Blocks to ignore in the configuration.
  --add-descriptions             Add descriptions inline with the code for all
                                 resource attributes.
  --required-blocks-only         Only include required blocks in the resource
                                 configuration.
  --required-attributes-only     Only include required attributes in the
                                 resource configuration.
  --help                         Show this message and exit.
```

# terraflow resource delete
Delete a resource from the configuration. 
## Usage
```
terraflow resource delete [OPTIONS]
```
## Options
```
  --terraform-filename TEXT  The name of the target Terraform file.
  --provider TEXT            The name of the Terraform provider.  [required]
  --namespace TEXT           The namespace of the Terraform provider.
                             [required]
  --name TEXT                The name to give the Terraform resource in the
                             configuration.  For example, 'main' or 'this'.
  --resource TEXT            The name of the terraform provider resource.
                             [required]
  --help                     Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow resource delete [OPTIONS]

  Delete a resource from the configuration.

Options:
  --terraform-filename TEXT  The name of the target Terraform file.
  --provider TEXT            The name of the Terraform provider.  [required]
  --namespace TEXT           The namespace of the Terraform provider.
                             [required]
  --name TEXT                The name to give the Terraform resource in the
                             configuration.  For example, 'main' or 'this'.
  --resource TEXT            The name of the terraform provider resource.
                             [required]
  --help                     Show this message and exit.
```

# terraflow data-source
Manage Terraform data sources. 
## Usage
```
terraflow data-source [OPTIONS] COMMAND [ARGS]...
```
## Options
```
  --help  Show this message and exit.
```
## Commands
```
  create  Create a data source.
  delete  Delete a data source from the configuration.
  list    List available data sources for a provider.
```
## CLI Help
```
Usage: terraflow data-source [OPTIONS] COMMAND [ARGS]...

  Manage Terraform data sources.

Options:
  --help  Show this message and exit.

Commands:
  create  Create a data source.
  delete  Delete a data source from the configuration.
  list    List available data sources for a provider.
```

# terraflow data-source list
List available data sources for a provider. 
## Usage
```
terraflow data-source list [OPTIONS]
```
## Options
```
  --provider TEXT   The name of the Terraform provider.  [required]
  --namespace TEXT  The namespace of the Terraform provider.  [required]
  --keyword TEXT    A keyword used to filter results.
  --help            Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow data-source list [OPTIONS]

  List available data sources for a provider.

Options:
  --provider TEXT   The name of the Terraform provider.  [required]
  --namespace TEXT  The namespace of the Terraform provider.  [required]
  --keyword TEXT    A keyword used to filter results.
  --help            Show this message and exit.
```

# terraflow data-source create
Create a data source. 
## Usage
```
terraflow data-source create [OPTIONS]
```
## Options
```
  --refresh                      Refresh the downloaded schema file.
  --schema-filename TEXT         The name of the Terraform schema to use
                                 locally.
  --terraform-filename TEXT      The name of the target Terraform file.
  --provider TEXT                The name of the Terraform provider.
                                 [required]
  --namespace TEXT               The namespace of the Terraform provider.
                                 [required]
  --name TEXT                    The name to give the Terraform resource in
                                 the configuration.  For example, 'main' or
                                 'this'.
  --resource TEXT                The name of the terraform provider resource.
                                 [required]
  --terraform-filename TEXT      The name of the target Terraform file.
  --attribute-value-prefix TEXT  A prefix to give to all variables in the
                                 resource configuration.  Useful for module
                                 development.
  --attribute-default TEXT       Default values for a given attributes in the
                                 format 'attribute=value'.
  --ignore-attribute TEXT        Attributes to ignore in the configuration.
  --dynamic-block TEXT           Blocks to make dynamic in the configuration.
  --ignore-block TEXT            Blocks to ignore in the configuration.
  --add-descriptions             Add descriptions inline with the code for all
                                 resource attributes.
  --required-blocks-only         Only include required blocks in the resource
                                 configuration.
  --required-attributes-only     Only include required attributes in the
                                 resource configuration.
  --help                         Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow data-source create [OPTIONS]

  Create a data source.

Options:
  --refresh                      Refresh the downloaded schema file.
  --schema-filename TEXT         The name of the Terraform schema to use
                                 locally.
  --terraform-filename TEXT      The name of the target Terraform file.
  --provider TEXT                The name of the Terraform provider.
                                 [required]
  --namespace TEXT               The namespace of the Terraform provider.
                                 [required]
  --name TEXT                    The name to give the Terraform resource in
                                 the configuration.  For example, 'main' or
                                 'this'.
  --resource TEXT                The name of the terraform provider resource.
                                 [required]
  --terraform-filename TEXT      The name of the target Terraform file.
  --attribute-value-prefix TEXT  A prefix to give to all variables in the
                                 resource configuration.  Useful for module
                                 development.
  --attribute-default TEXT       Default values for a given attributes in the
                                 format 'attribute=value'.
  --ignore-attribute TEXT        Attributes to ignore in the configuration.
  --dynamic-block TEXT           Blocks to make dynamic in the configuration.
  --ignore-block TEXT            Blocks to ignore in the configuration.
  --add-descriptions             Add descriptions inline with the code for all
                                 resource attributes.
  --required-blocks-only         Only include required blocks in the resource
                                 configuration.
  --required-attributes-only     Only include required attributes in the
                                 resource configuration.
  --help                         Show this message and exit.
```

# terraflow data-source delete
Delete a data source from the configuration. 
## Usage
```
terraflow data-source delete [OPTIONS]
```
## Options
```
  --terraform-filename TEXT  The name of the target Terraform file.
  --provider TEXT            The name of the Terraform provider.  [required]
  --namespace TEXT           The namespace of the Terraform provider.
                             [required]
  --name TEXT                The name to give the Terraform resource in the
                             configuration.  For example, 'main' or 'this'.
  --resource TEXT            The name of the terraform provider resource.
                             [required]
  --help                     Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow data-source delete [OPTIONS]

  Delete a data source from the configuration.

Options:
  --terraform-filename TEXT  The name of the target Terraform file.
  --provider TEXT            The name of the Terraform provider.  [required]
  --namespace TEXT           The namespace of the Terraform provider.
                             [required]
  --name TEXT                The name to give the Terraform resource in the
                             configuration.  For example, 'main' or 'this'.
  --resource TEXT            The name of the terraform provider resource.
                             [required]
  --help                     Show this message and exit.
```

# terraflow provider
Manage Terraform providers. 
## Usage
```
terraflow provider [OPTIONS] COMMAND [ARGS]...
```
## Options
```
  --help  Show this message and exit.
```
## Commands
```
  create  Create a provider.
  delete  Delete a provider from the configuration.
  list    List providers in the Terraform configuration.
```
## CLI Help
```
Usage: terraflow provider [OPTIONS] COMMAND [ARGS]...

  Manage Terraform providers.

Options:
  --help  Show this message and exit.

Commands:
  create  Create a provider.
  delete  Delete a provider from the configuration.
  list    List providers in the Terraform configuration.
```

# terraflow provider list
List providers in the Terraform configuration. 
## Usage
```
terraflow provider list [OPTIONS]
```
## Options
```
  --keyword TEXT  A keyword used to filter results.
  --help          Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow provider list [OPTIONS]

  List providers in the Terraform configuration.

Options:
  --keyword TEXT  A keyword used to filter results.
  --help          Show this message and exit.
```

# terraflow provider create
Create a provider. 
## Usage
```
terraflow provider create [OPTIONS]
```
## Options
```
  --refresh                      Refresh the downloaded schema file.
  --schema-filename TEXT         The name of the Terraform schema to use
                                 locally.
  --terraform-filename TEXT      The name of the target Terraform file.
  --provider TEXT                The name of the Terraform provider.
                                 [required]
  --namespace TEXT               The namespace of the Terraform provider.
                                 [required]
  --terraform-filename TEXT      The name of the target Terraform file.
  --attribute-value-prefix TEXT  A prefix to give to all variables in the
                                 resource configuration.  Useful for module
                                 development.
  --attribute-default TEXT       Default values for a given attributes in the
                                 format 'attribute=value'.
  --ignore-attribute TEXT        Attributes to ignore in the configuration.
  --dynamic-block TEXT           Blocks to make dynamic in the configuration.
  --ignore-block TEXT            Blocks to ignore in the configuration.
  --add-descriptions             Add descriptions inline with the code for all
                                 resource attributes.
  --required-blocks-only         Only include required blocks in the resource
                                 configuration.
  --required-attributes-only     Only include required attributes in the
                                 resource configuration.
  --help                         Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow provider create [OPTIONS]

  Create a provider.

Options:
  --refresh                      Refresh the downloaded schema file.
  --schema-filename TEXT         The name of the Terraform schema to use
                                 locally.
  --terraform-filename TEXT      The name of the target Terraform file.
  --provider TEXT                The name of the Terraform provider.
                                 [required]
  --namespace TEXT               The namespace of the Terraform provider.
                                 [required]
  --terraform-filename TEXT      The name of the target Terraform file.
  --attribute-value-prefix TEXT  A prefix to give to all variables in the
                                 resource configuration.  Useful for module
                                 development.
  --attribute-default TEXT       Default values for a given attributes in the
                                 format 'attribute=value'.
  --ignore-attribute TEXT        Attributes to ignore in the configuration.
  --dynamic-block TEXT           Blocks to make dynamic in the configuration.
  --ignore-block TEXT            Blocks to ignore in the configuration.
  --add-descriptions             Add descriptions inline with the code for all
                                 resource attributes.
  --required-blocks-only         Only include required blocks in the resource
                                 configuration.
  --required-attributes-only     Only include required attributes in the
                                 resource configuration.
  --help                         Show this message and exit.
```

# terraflow provider delete
Delete a provider from the configuration. 
## Usage
```
terraflow provider delete [OPTIONS]
```
## Options
```
  --terraform-filename TEXT  The name of the target Terraform file.
  --provider TEXT            The name of the Terraform provider.  [required]
  --namespace TEXT           The namespace of the Terraform provider.
                             [required]
  --help                     Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow provider delete [OPTIONS]

  Delete a provider from the configuration.

Options:
  --terraform-filename TEXT  The name of the target Terraform file.
  --provider TEXT            The name of the Terraform provider.  [required]
  --namespace TEXT           The namespace of the Terraform provider.
                             [required]
  --help                     Show this message and exit.
```

# terraflow docs
Manage documentation. 
## Usage
```
terraflow docs [OPTIONS] COMMAND [ARGS]...
```
## Options
```
  --help  Show this message and exit.
```
## Commands
```
  create  Generate Terraform documentation using terraform-docs.
```
## CLI Help
```
Usage: terraflow docs [OPTIONS] COMMAND [ARGS]...

  Manage documentation.

Options:
  --help  Show this message and exit.

Commands:
  create  Generate Terraform documentation using terraform-docs.
```

# terraflow docs create
Generate Terraform documentation using terraform-docs.    This command generates a markdown table of the Terraform module's   configuration and saves it to a README.md file in the module's directory. 
## Usage
```
terraflow docs create [OPTIONS]
```
## Options
```
  --module-path TEXT      Path to the Terraform module  [required]
  --config-filename TEXT  Filename for the terraform-docs configuration file
  --help                  Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow docs create [OPTIONS]

  Generate Terraform documentation using terraform-docs.

  This command generates a markdown table of the Terraform module's
  configuration and saves it to a README.md file in the module's directory.

Options:
  --module-path TEXT      Path to the Terraform module  [required]
  --config-filename TEXT  Filename for the terraform-docs configuration file
  --help                  Show this message and exit.
```

