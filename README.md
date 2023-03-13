# I want to accelerate development of Terraform
# To do this, I want to dynamically generate Terraform resource code
# As part of dynamic resource generation I would like to be able to:
# [x] Determine the target file for the resource
# [x] If a file does not exist have it automatically created
# [x] Have the option to change the write mode from append (default) to override
# [x] Name the resource
# [x] Create resource based on a specific provider version
# [x] Add all resource attributes
# [x] Filter out computed resource attributes
# [x] Filter out non-required resource attributes
# [x] Add a default variable for the attribute
# [x] Add a prefix to variables
# [x] Automatically add descriptions to attributes
# [ ] Add variables to a variables file automatically
# [ ] Select the name and location of the variables file
# [x] Use block names in the name of nested variables
# [x] Set default values for specific variables (static or reference)
# [x] Add comments to blocks to specify if they are required or not
# [x] Add comments to blocks to specify if more than one are allowed
# [ ] Make blocks that allow more than one item dynamic by default

# CLI commands
# tool-name 

# terraform-ai boot
# terraform-ai workspace set
# terraform-ai workspace get
# terraform-ai workspace list
# terraform-ai workspace create
# terraform-ai workspace delete
# terraform-ai schema download
# terraform-ai resource create --namespace --provider --provider-version --name
# terraform-ai variable create --namespace --provider --provider-version --name
# terraform-ai provider create --namespace --provider --provider-version
# terraform-ai documentation create --namespace --provider --provider-version --name --readme-file-name

# Documentation prompt: I am creating a Terraform module using azurerm_storagez_account.  Help me write the documentation for the module.  Don't provide code examples and don't use the resource name in the description.  It should be a single paragraph that describes what the module is used for.  Don't talk about other services that might be part of the module.