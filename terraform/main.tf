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

resource "azurerm_resource_group" "main" {
  location = var.location
  name     = var.name
}