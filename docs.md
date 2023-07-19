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
  data      Manage Terraform data sources.
  provider  Manage Terraform providers.
  resource  Manage Terraform resources.
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
  data      Manage Terraform data sources.
  provider  Manage Terraform providers.
  resource  Manage Terraform resources.
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
  create  Create a Terraform provider.
  get     Get providers in the Terraform configuration.
  list    List available providers.
```
## CLI Help
```
Usage: terraflow provider [OPTIONS] COMMAND [ARGS]...

  Manage Terraform providers.

Options:
  --help  Show this message and exit.

Commands:
  create  Create a Terraform provider.
  get     Get providers in the Terraform configuration.
  list    List available providers.
```

# terraflow provider list
List available providers. 
## Usage
```
terraflow provider list [OPTIONS]
```
## Options
```
  --provider TEXT   The name of the Terraform provider.  [required]
  --namespace TEXT  The namespace of the Terraform provider.  [required]
  --help            Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow provider list [OPTIONS]

  List available providers.

Options:
  --provider TEXT   The name of the Terraform provider.  [required]
  --namespace TEXT  The namespace of the Terraform provider.  [required]
  --help            Show this message and exit.
```

# terraflow provider get
Get providers in the Terraform configuration. 
## Usage
```
terraflow provider get [OPTIONS]
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
Usage: terraflow provider get [OPTIONS]

  Get providers in the Terraform configuration.

Options:
  --keyword TEXT  A keyword used to filter results.
  --help          Show this message and exit.
```

# terraflow provider create
Create a Terraform provider. 
## Usage
```
terraflow provider create [OPTIONS]
```
## Options
```
  --refresh                      Refresh the downloaded schema file.
  --terraform-filename TEXT      The name of file to store Terraform resources
                                 in.
  --provider TEXT                The name of the Terraform provider.
                                 [required]
  --namespace TEXT               The namespace of the Terraform provider.
                                 [required]
  --header-comment TEXT          A comment to add to the header of the
                                 resource.
  --terraform-filename TEXT      The name of file to store Terraform resources
                                 in.
  --attribute-value-prefix TEXT  A prefix to give to all variables in the
                                 resource configuration.  Useful for module
                                 development.
  --attribute-default TEXT       Default values for a given attributes in the
                                 format 'attribute=value'.
  --exclude-attribute TEXT       Attributes to exclude in the configuration.
  --exclude-block TEXT           Blocks to exclude in the configuration.
  --add-terraform-docs-url       Add a link to the documentation above the
                                 resource.
  --add-inline-descriptions      Add descriptions inline with the code for all
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

  Create a Terraform provider.

Options:
  --refresh                      Refresh the downloaded schema file.
  --terraform-filename TEXT      The name of file to store Terraform resources
                                 in.
  --provider TEXT                The name of the Terraform provider.
                                 [required]
  --namespace TEXT               The namespace of the Terraform provider.
                                 [required]
  --header-comment TEXT          A comment to add to the header of the
                                 resource.
  --terraform-filename TEXT      The name of file to store Terraform resources
                                 in.
  --attribute-value-prefix TEXT  A prefix to give to all variables in the
                                 resource configuration.  Useful for module
                                 development.
  --attribute-default TEXT       Default values for a given attributes in the
                                 format 'attribute=value'.
  --exclude-attribute TEXT       Attributes to exclude in the configuration.
  --exclude-block TEXT           Blocks to exclude in the configuration.
  --add-terraform-docs-url       Add a link to the documentation above the
                                 resource.
  --add-inline-descriptions      Add descriptions inline with the code for all
                                 resource attributes.
  --required-blocks-only         Only include required blocks in the resource
                                 configuration.
  --required-attributes-only     Only include required attributes in the
                                 resource configuration.
  --help                         Show this message and exit.
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
  --terraform-filename TEXT      The name of file to store Terraform resources
                                 in.
  --provider TEXT                The name of the Terraform provider.
                                 [required]
  --namespace TEXT               The namespace of the Terraform provider.
                                 [required]
  --name TEXT                    The name to give the Terraform resource in
                                 the configuration.  For example, 'main' or
                                 'this'.
  --kind TEXT                    The name of the terraform provider resource.
                                 [required]
  --header-comment TEXT          A comment to add to the header of the
                                 resource.
  --terraform-filename TEXT      The name of file to store Terraform resources
                                 in.
  --attribute-value-prefix TEXT  A prefix to give to all variables in the
                                 resource configuration.  Useful for module
                                 development.
  --attribute-default TEXT       Default values for a given attributes in the
                                 format 'attribute=value'.
  --exclude-attribute TEXT       Attributes to exclude in the configuration.
  --exclude-block TEXT           Blocks to exclude in the configuration.
  --add-terraform-docs-url       Add a link to the documentation above the
                                 resource.
  --add-inline-descriptions      Add descriptions inline with the code for all
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
  --terraform-filename TEXT      The name of file to store Terraform resources
                                 in.
  --provider TEXT                The name of the Terraform provider.
                                 [required]
  --namespace TEXT               The namespace of the Terraform provider.
                                 [required]
  --name TEXT                    The name to give the Terraform resource in
                                 the configuration.  For example, 'main' or
                                 'this'.
  --kind TEXT                    The name of the terraform provider resource.
                                 [required]
  --header-comment TEXT          A comment to add to the header of the
                                 resource.
  --terraform-filename TEXT      The name of file to store Terraform resources
                                 in.
  --attribute-value-prefix TEXT  A prefix to give to all variables in the
                                 resource configuration.  Useful for module
                                 development.
  --attribute-default TEXT       Default values for a given attributes in the
                                 format 'attribute=value'.
  --exclude-attribute TEXT       Attributes to exclude in the configuration.
  --exclude-block TEXT           Blocks to exclude in the configuration.
  --add-terraform-docs-url       Add a link to the documentation above the
                                 resource.
  --add-inline-descriptions      Add descriptions inline with the code for all
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
  --provider TEXT   The name of the Terraform provider.  [required]
  --namespace TEXT  The namespace of the Terraform provider.  [required]
  --name TEXT       The name to give the Terraform resource in the
                    configuration.  For example, 'main' or 'this'.
  --kind TEXT       The name of the terraform provider resource.  [required]
  --help            Show this message and exit.
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
  --provider TEXT   The name of the Terraform provider.  [required]
  --namespace TEXT  The namespace of the Terraform provider.  [required]
  --name TEXT       The name to give the Terraform resource in the
                    configuration.  For example, 'main' or 'this'.
  --kind TEXT       The name of the terraform provider resource.  [required]
  --help            Show this message and exit.
```

# terraflow data
Manage Terraform data sources. 
## Usage
```
terraflow data [OPTIONS] COMMAND [ARGS]...
```
## Options
```
  --help  Show this message and exit.
```
## Commands
```
  create  Create a Terraform data source.
  delete  Delete a data source from the configuration.
  list    List available data sources for a provider.
```
## CLI Help
```
Usage: terraflow data [OPTIONS] COMMAND [ARGS]...

  Manage Terraform data sources.

Options:
  --help  Show this message and exit.

Commands:
  create  Create a Terraform data source.
  delete  Delete a data source from the configuration.
  list    List available data sources for a provider.
```

# terraflow data list
List available data sources for a provider. 
## Usage
```
terraflow data list [OPTIONS]
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
Usage: terraflow data list [OPTIONS]

  List available data sources for a provider.

Options:
  --provider TEXT   The name of the Terraform provider.  [required]
  --namespace TEXT  The namespace of the Terraform provider.  [required]
  --keyword TEXT    A keyword used to filter results.
  --help            Show this message and exit.
```

# terraflow data create
Create a Terraform data source. 
## Usage
```
terraflow data create [OPTIONS]
```
## Options
```
  --refresh                      Refresh the downloaded schema file.
  --terraform-filename TEXT      The name of file to store Terraform resources
                                 in.
  --provider TEXT                The name of the Terraform provider.
                                 [required]
  --namespace TEXT               The namespace of the Terraform provider.
                                 [required]
  --name TEXT                    The name to give the Terraform resource in
                                 the configuration.  For example, 'main' or
                                 'this'.
  --kind TEXT                    The name of the terraform provider resource.
                                 [required]
  --header-comment TEXT          A comment to add to the header of the
                                 resource.
  --terraform-filename TEXT      The name of file to store Terraform resources
                                 in.
  --attribute-value-prefix TEXT  A prefix to give to all variables in the
                                 resource configuration.  Useful for module
                                 development.
  --attribute-default TEXT       Default values for a given attributes in the
                                 format 'attribute=value'.
  --exclude-attribute TEXT       Attributes to exclude in the configuration.
  --exclude-block TEXT           Blocks to exclude in the configuration.
  --add-terraform-docs-url       Add a link to the documentation above the
                                 resource.
  --add-inline-descriptions      Add descriptions inline with the code for all
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
Usage: terraflow data create [OPTIONS]

  Create a Terraform data source.

Options:
  --refresh                      Refresh the downloaded schema file.
  --terraform-filename TEXT      The name of file to store Terraform resources
                                 in.
  --provider TEXT                The name of the Terraform provider.
                                 [required]
  --namespace TEXT               The namespace of the Terraform provider.
                                 [required]
  --name TEXT                    The name to give the Terraform resource in
                                 the configuration.  For example, 'main' or
                                 'this'.
  --kind TEXT                    The name of the terraform provider resource.
                                 [required]
  --header-comment TEXT          A comment to add to the header of the
                                 resource.
  --terraform-filename TEXT      The name of file to store Terraform resources
                                 in.
  --attribute-value-prefix TEXT  A prefix to give to all variables in the
                                 resource configuration.  Useful for module
                                 development.
  --attribute-default TEXT       Default values for a given attributes in the
                                 format 'attribute=value'.
  --exclude-attribute TEXT       Attributes to exclude in the configuration.
  --exclude-block TEXT           Blocks to exclude in the configuration.
  --add-terraform-docs-url       Add a link to the documentation above the
                                 resource.
  --add-inline-descriptions      Add descriptions inline with the code for all
                                 resource attributes.
  --required-blocks-only         Only include required blocks in the resource
                                 configuration.
  --required-attributes-only     Only include required attributes in the
                                 resource configuration.
  --help                         Show this message and exit.
```

# terraflow data delete
Delete a data source from the configuration. 
## Usage
```
terraflow data delete [OPTIONS]
```
## Options
```
  --provider TEXT   The name of the Terraform provider.  [required]
  --namespace TEXT  The namespace of the Terraform provider.  [required]
  --name TEXT       The name to give the Terraform resource in the
                    configuration.  For example, 'main' or 'this'.
  --kind TEXT       The name of the terraform provider resource.  [required]
  --help            Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow data delete [OPTIONS]

  Delete a data source from the configuration.

Options:
  --provider TEXT   The name of the Terraform provider.  [required]
  --namespace TEXT  The namespace of the Terraform provider.  [required]
  --name TEXT       The name to give the Terraform resource in the
                    configuration.  For example, 'main' or 'this'.
  --kind TEXT       The name of the terraform provider resource.  [required]
  --help            Show this message and exit.
```

