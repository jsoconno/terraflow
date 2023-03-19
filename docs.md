# terraflow
Terraform is an open-source infrastructure as code tool that    allows developers to manage cloud resources through code.    Terraflow provides developers with a set of commands and features    that can help them create, test, and deploy Terraform code more efficiently.    With Terraflow, developers can easily create Terraform modules, templates,   and configurations using a simple and intuitive command line interface.   They can also quickly generate code snippets and boilerplate code, reducing   the amount of manual work required to create new Terraform resources. 
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
  boot         Docs
  data-source  Docs
  provider     Docs
  resource     Docs
  schema       Schema management.
  workspace    Docs
```
## CLI Help
```
Usage: terraflow [OPTIONS] COMMAND [ARGS]...

  Terraform is an open-source infrastructure as code tool that 
  allows developers to manage cloud resources through code. 
  Terraflow provides developers with a set of commands and features 
  that can help them create, test, and deploy Terraform code more efficiently.

  With Terraflow, developers can easily create Terraform modules, templates,
  and configurations using a simple and intuitive command line interface.
  They can also quickly generate code snippets and boilerplate code, reducing
  the amount of manual work required to create new Terraform resources.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  boot         Docs
  data-source  Docs
  provider     Docs
  resource     Docs
  schema       Schema management.
  workspace    Docs
```

# terraflow boot
Docs 
## Usage
```
terraflow boot [OPTIONS] COMMAND [ARGS]...
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
Usage: terraflow boot [OPTIONS] COMMAND [ARGS]...

  Docs

Options:
  --help  Show this message and exit.
```

# terraflow workspace
Docs 
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
  list    Get workspaces.
  set     Set a workspace.
```
## CLI Help
```
Usage: terraflow workspace [OPTIONS] COMMAND [ARGS]...

  Docs

Options:
  --help  Show this message and exit.

Commands:
  create  Create a workspace.
  delete  Delete a workspace.
  get     Get a workspace.
  list    Get workspaces.
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
Get workspaces. 
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

  Get workspaces.

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
Schema management. 
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
  download
```
## CLI Help
```
Usage: terraflow schema [OPTIONS] COMMAND [ARGS]...

  Schema management.

Options:
  --help  Show this message and exit.

Commands:
  download
```

# terraflow schema download

## Usage
```
terraflow schema download [OPTIONS]
```
## Options
```
  --filename TEXT
  --help           Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow schema download [OPTIONS]

Options:
  --filename TEXT
  --help           Show this message and exit.
```

# terraflow resource
Docs 
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
  create  Docs
  list
```
## CLI Help
```
Usage: terraflow resource [OPTIONS] COMMAND [ARGS]...

  Docs

Options:
  --help  Show this message and exit.

Commands:
  create  Docs
  list
```

# terraflow resource list

## Usage
```
terraflow resource list [OPTIONS]
```
## Options
```
  --provider TEXT   The name of the Terraform provider.  [required]
  --namespace TEXT  The namespace for the Terraform provider.  [required]
  --keyword TEXT    Keyword used to filter the list.
  --help            Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow resource list [OPTIONS]

Options:
  --provider TEXT   The name of the Terraform provider.  [required]
  --namespace TEXT  The namespace for the Terraform provider.  [required]
  --keyword TEXT    Keyword used to filter the list.
  --help            Show this message and exit.
```

# terraflow resource create
Docs 
## Usage
```
terraflow resource create [OPTIONS]
```
## Options
```
  --schema TEXT                  The name of the schema to use for resource
                                 creation.
  --provider TEXT                The name of the Terraform provider.
                                 [required]
  --namespace TEXT               The namespace for the Terraform provider.
                                 [required]
  --name TEXT                    The name of the resource or data source.
  --resource TEXT                The target Terraform resource name.
                                 [required]
  --filename TEXT
  --attribute-value-prefix TEXT
  --attribute-default TEXT
  --ignore-attribute TEXT
  --dynamic-block TEXT
  --ignore-block TEXT
  --add-descriptions
  --required-blocks-only
  --required-attributes-only
  --help                         Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow resource create [OPTIONS]

  Docs

Options:
  --schema TEXT                  The name of the schema to use for resource
                                 creation.
  --provider TEXT                The name of the Terraform provider.
                                 [required]
  --namespace TEXT               The namespace for the Terraform provider.
                                 [required]
  --name TEXT                    The name of the resource or data source.
  --resource TEXT                The target Terraform resource name.
                                 [required]
  --filename TEXT
  --attribute-value-prefix TEXT
  --attribute-default TEXT
  --ignore-attribute TEXT
  --dynamic-block TEXT
  --ignore-block TEXT
  --add-descriptions
  --required-blocks-only
  --required-attributes-only
  --help                         Show this message and exit.
```

# terraflow data-source
Docs 
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
  create  Docs
  list
```
## CLI Help
```
Usage: terraflow data-source [OPTIONS] COMMAND [ARGS]...

  Docs

Options:
  --help  Show this message and exit.

Commands:
  create  Docs
  list
```

# terraflow data-source list

## Usage
```
terraflow data-source list [OPTIONS]
```
## Options
```
  --provider TEXT   The name of the Terraform provider.  [required]
  --namespace TEXT  The namespace for the Terraform provider.  [required]
  --keyword TEXT    Keyword used to filter the list.
  --help            Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow data-source list [OPTIONS]

Options:
  --provider TEXT   The name of the Terraform provider.  [required]
  --namespace TEXT  The namespace for the Terraform provider.  [required]
  --keyword TEXT    Keyword used to filter the list.
  --help            Show this message and exit.
```

# terraflow data-source create
Docs 
## Usage
```
terraflow data-source create [OPTIONS]
```
## Options
```
  --schema TEXT                  The name of the schema to use for resource
                                 creation.
  --provider TEXT                The name of the Terraform provider.
                                 [required]
  --namespace TEXT               The namespace for the Terraform provider.
                                 [required]
  --name TEXT                    The name of the resource or data source.
  --resource TEXT                The target Terraform resource name.
                                 [required]
  --filename TEXT
  --attribute-value-prefix TEXT
  --attribute-default TEXT
  --ignore-attribute TEXT
  --dynamic-block TEXT
  --ignore-block TEXT
  --add-descriptions
  --required-blocks-only
  --required-attributes-only
  --help                         Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow data-source create [OPTIONS]

  Docs

Options:
  --schema TEXT                  The name of the schema to use for resource
                                 creation.
  --provider TEXT                The name of the Terraform provider.
                                 [required]
  --namespace TEXT               The namespace for the Terraform provider.
                                 [required]
  --name TEXT                    The name of the resource or data source.
  --resource TEXT                The target Terraform resource name.
                                 [required]
  --filename TEXT
  --attribute-value-prefix TEXT
  --attribute-default TEXT
  --ignore-attribute TEXT
  --dynamic-block TEXT
  --ignore-block TEXT
  --add-descriptions
  --required-blocks-only
  --required-attributes-only
  --help                         Show this message and exit.
```

# terraflow provider
Docs 
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
  create  Docs
  list
```
## CLI Help
```
Usage: terraflow provider [OPTIONS] COMMAND [ARGS]...

  Docs

Options:
  --help  Show this message and exit.

Commands:
  create  Docs
  list
```

# terraflow provider list

## Usage
```
terraflow provider list [OPTIONS]
```
## Options
```
  --keyword TEXT  Keyword used to filter the list.
  --help          Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow provider list [OPTIONS]

Options:
  --keyword TEXT  Keyword used to filter the list.
  --help          Show this message and exit.
```

# terraflow provider create
Docs 
## Usage
```
terraflow provider create [OPTIONS]
```
## Options
```
  --schema TEXT                  The name of the schema to use for resource
                                 creation.
  --provider TEXT                The name of the Terraform provider.
                                 [required]
  --namespace TEXT               The namespace for the Terraform provider.
                                 [required]
  --filename TEXT
  --attribute-value-prefix TEXT
  --attribute-default TEXT
  --ignore-attribute TEXT
  --dynamic-block TEXT
  --ignore-block TEXT
  --add-descriptions
  --required-blocks-only
  --required-attributes-only
  --help                         Show this message and exit.
```
## Commands
```
None
```
## CLI Help
```
Usage: terraflow provider create [OPTIONS]

  Docs

Options:
  --schema TEXT                  The name of the schema to use for resource
                                 creation.
  --provider TEXT                The name of the Terraform provider.
                                 [required]
  --namespace TEXT               The namespace for the Terraform provider.
                                 [required]
  --filename TEXT
  --attribute-value-prefix TEXT
  --attribute-default TEXT
  --ignore-attribute TEXT
  --dynamic-block TEXT
  --ignore-block TEXT
  --add-descriptions
  --required-blocks-only
  --required-attributes-only
  --help                         Show this message and exit.
```

