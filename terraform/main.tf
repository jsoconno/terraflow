/**
* # Main title
*
* Everything in this comment block will get extracted into docs.
*
* You can put simple text or complete Markdown content
* here. Subsequently if you want to render AsciiDoc format
* you can put AsciiDoc compatible content in this comment
* block.
*/

# What is the industry best practice?

# What is the strongest use case?
## End of April
# - Acceleration for stubbing out code
# - Automated collection of documentation
# - Dynamic creation of variables and outputs
# - Handy functionaly for automatically writing logic
## End of May
# - Automated documentation
## End of June
# - Wrapper for Terraform commands with additional functionality
## July to September
# - A compiled Terraform framework
# - AI embedded (automated documentation of module, resource recommentations, auto-security hardening)

# What do you do about generating variables.tf?
# - terraflow resource create --provider azurerm --resource resource_group --auto-generate-vars
# - terraflow resource create --provider azurerm --resource storage_account --inherit-attribute-values azurerm_resource_group.main
# - terraflow variable create --name my_var --type list --description 'whatever'

# What do you do about modules?
# - 