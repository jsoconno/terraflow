"""
Constant values used across the CLI.
"""
import os

ALLOWED_SCOPES = ["data_source", "resource", "provider"]
TERRAFLOW_DIR = ".terraflow"
DOCUMENTATION_DIR = os.path.join(TERRAFLOW_DIR, "documentation")
TERRAFORM_REGISTRY_BASE = "registry.terraform.io"
GITHUB_BASE = "github.com"
VALID_TYPES = {"string", "number", "bool", "list", "map", "set", "object", "tuple", "any"}
