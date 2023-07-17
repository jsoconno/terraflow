import os
import re
import requests
from bs4 import BeautifulSoup

from terraflow.libraries.constants import DOCUMENTATION_DIR, TERRAFORM_REGISTRY_BASE, GITHUB_BASE
from terraflow.libraries.helpers import scrape_website

class TerraformDocumentation:
    def __init__(self, namespace, provider, version='main', kind=None, type=None, use_cache=True, refresh=False):
        self.namespace = namespace
        self.provider = provider
        self.version = version
        self.kind = kind
        self.type = type
        self.use_cache = use_cache
        self.refresh = refresh

        self.url = self._get_docs_url()
        self.text = self._get_docs_text()
        self.inputs = self._get_inputs(self.text)
        self.outputs = self._get_outputs(self.text)

    def _get_docs_url(self):
        if self.type == 'provider':
            return f"https://{GITHUB_BASE}/{self.namespace}/terraform-provider-{self.provider}/blob/{'' if self.version == 'main' else 'v'}{self.version}/website/docs/index.html.markdown"
        elif self.type == 'resource':
            return f"https://{GITHUB_BASE}/{self.namespace}/terraform-provider-{self.provider}/blob/{'' if self.version == 'main' else 'v'}{self.version}/website/docs/r/{self.kind}.html.markdown"
        elif self.type == 'data':
            return f"https://{GITHUB_BASE}/{self.namespace}/terraform-provider-{self.provider}/blob/{'' if self.version == 'main' else 'v'}{self.version}/website/docs/d/{self.kind}.html.markdown"
        else:
            raise ValueError("Invalid scope. Must be one of 'provider', 'resource', or 'data'.")
        
    def _get_docs_text(self):
        # Check is the user wants to use cache documentation
        if self.use_cache:
            # Set the documentation directory
            documentation_dir = os.path.join(DOCUMENTATION_DIR, self.namespace, self.provider, self.version)

            # Set the filepath
            if self.type == 'provider':
                filepath = os.path.join(documentation_dir)
            else:
                filepath = os.path.join(documentation_dir, self.kind)
            
            # Determine if the documentation directory exists, and if not, create it
            if not os.path.exists(filepath):
                os.makedirs(filepath)

            # If the file exists
            if os.path.exists(filepath + f'/{self.type}.txt'):
                # If refresh is True
                if self.refresh:
                    # Srape the documentation and write it to file
                    text = scrape_website(self.url, tag='article')
                    with open(filepath + f'/{self.type}.txt', 'w') as f:
                        f.write(text)
                        return text
                else:
                    # Read the existing documentation from file
                    with open(filepath + f'/{self.type}.txt', 'r') as f:
                        text = f.read()
                        return text
            else:
                # Srape the documentation and write it to file
                text = scrape_website(self.url, tag='article')
                with open(filepath + f'/{self.type}.txt', 'w') as f:
                    f.write(text)
                    return text

        else:
            # Srape the documentation and write it to file
            text = scrape_website(self.url, tag='article')
            return text
        
    def _get_inputs(self, documentation):
        pattern = r'^Argument(?:s)? Reference([\s\S]*?)^Attribute(?:s)? Reference'
        matches = re.findall(pattern, documentation, re.MULTILINE)

        if matches:
            argument_section = matches[0].strip()
            argument_pattern = r"([\w_]+) -"
            argument_references = re.findall(argument_pattern, argument_section)
            arguments = []
            for argument_name in argument_references:
                arguments.append({
                    "name": argument_name,
                    "description": "",  # You can parse the description from the documentation text if desired
                    "required": False,  # You can parse the required status from the documentation text if desired
                    "default": ""  # You can parse the default value from the documentation text if desired
                })
            return arguments

        return []
    
    def _get_outputs(self, documentation):
        pattern = r'^Attribute(?:s)? Reference([\s\S]*?)^Import'
        matches = re.findall(pattern, documentation, re.MULTILINE)

        if matches:
            attribute_section = matches[0].strip()
            attribute_pattern = r"([\w_]+) -"
            attribute_references = re.findall(attribute_pattern, attribute_section)
            attributes = []
            for attribute_name in attribute_references:
                attributes.append({
                    "name": attribute_name,
                    "description": ""  # You can parse the description from the documentation text if desired
                })
            return attributes

        return []
