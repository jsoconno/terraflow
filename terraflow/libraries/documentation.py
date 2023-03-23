import os
import subprocess
import yaml

from terraflow.libraries.core import colors, get_terraform_provider_versions


def is_terraform_docs_installed():
    try:
        subprocess.run(
            ["terraform-docs", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except FileNotFoundError:
        return False


def install_terraform_docs():
    if not is_terraform_docs_installed():
        try:
            subprocess.run(
                [
                    "curl",
                    "-sSLo",
                    "terraform-docs",
                    "https://github.com/terraform-docs/terraform-docs/releases/latest/download/terraform-docs",
                ],
                check=True,
            )
            subprocess.run(["chmod", "+x", "terraform-docs"], check=True)
            subprocess.run(["mv", "terraform-docs", "/usr/local/bin/"], check=True)
            print(
                f'\n{colors(color="OK_GREEN")}Terraform-docs successfully installed.{colors()}\n'
            )
        except subprocess.CalledProcessError as e:
            print(
                f'\n{colors(color="FAIL")}Failed to install terraform-docs:{colors()} {e}\n'
            )
    else:
        print(
            f'\n{colors(color="OK_GREEN")}terraform-docs is already installed.{colors()}\n'
        )

def create_terraform_file(filename, filepath=".", content=""):
    # Create the module path if it does not exist
    if filepath and not os.path.exists(filepath):
        os.makedirs(filepath)

    file_path = os.path.join(filepath, filename)
    with open(file_path, "w") as f:
        f.write(content)

def create_terraform_main_file(filepath="."):
    content = """/**
    * # Main title
    *
    * Everything in this comment block will get extracted into docs.
    *
    * You can put simple text or complete Markdown content
    * here. Subsequently if you want to render AsciiDoc format
    * you can put AsciiDoc compatible content in this comment
    * block.
    */\n\n"""

    create_terraform_file(
        filename="main.tf",
        filepath=filepath,
        content=content
    )

def create_terraform_versions_file(filepath=".", terraform_version=">= 1.0.0", namespace="hashicorp", providers=[]):
    content = "terraform {\n"

    if terraform_version:
        content += f'  required_version = "{terraform_version}"\n'

    if providers:
        content += '  required_providers {\n'
        for provider in providers:
            latest_version = get_terraform_provider_versions(namespace=namespace, provider=provider)[-1]
            content += f'    {provider} = {{\n'
            content += f'      source = "{namespace}/{provider}"\n'
            content += f'      version = "{latest_version}"\n'
            content += '    }\n'
        content += '  }\n'
    content += '}\n'

    create_terraform_file(
        filename="versions.tf",
        filepath=filepath,
        content=content
    )

def create_terraform_docs_config_file(filepath=".", sort_by="name"):
    content = {
        "formatter": "markdown",
        "version": "",
        "header-from": "main.tf",
        "footer-from": "",
        "recursive": {
            "enabled": False,
            "path": "modules",
        },
        "sections": {
            "hide": [],
            "show": [],
            "hide-all": False,
            "show-all": True,
        },
        "content": "",
        "output": {
            "file": "",
            "mode": "inject",
            "template": "<!-- BEGIN_TF_DOCS -->\n{{ .Content }}\n<!-- END_TF_DOCS -->",
        },
        "output-values": {
            "enabled": False,
            "from": "",
        },
        "sort": {
            "enabled": True,
            "by": "name",
        },
        "settings": {
            "anchor": True,
            "color": True,
            "default": True,
            "description": False,
            "escape": True,
            "hide-empty": False,
            "html": True,
            "indent": 2,
            "lockfile": True,
            "read-comments": True,
            "required": True,
            "sensitive": True,
            "type": True,
        },
    }

    create_terraform_file(
        filename="terraform-docs.yaml",
        filepath=filepath,
        content=yaml.dump(content)
    )


def generate_terraform_docs(module_path=".", config_filename="terraform-docs.yaml"):
    if not is_terraform_docs_installed():
        install_terraform_docs()

    try:
        docs = subprocess.run(
            ["terraform-docs", "--config", config_filename, module_path],
            check=True,
            capture_output=True,
            text=True,
        )
        print(
            f'\n{colors(color="OK_GREEN")}Generated Terraform documentation in {os.path.join(module_path, "README.md")}{colors()}\n'
        )

        with open("README.md", "w") as file:
            file.write(docs.stdout)

    except subprocess.CalledProcessError as e:
        print(
            f'\n{colors(color="FAIL")}Failed to generate Terraform documentation:{colors()} {e}\n'
        )

def initialize_terraform_module(filepath=".", terraform_version=">= 1.0.0", namespace="hashicorp", providers=[], add_terraform_docs_config_file=False):
    create_terraform_main_file(
        filepath=filepath
    )
    create_terraform_versions_file(
        filepath=filepath,
        terraform_version=terraform_version,
        namespace=namespace,
        providers=providers
    )
    create_terraform_file(
        filename='data-sources.tf',
        filepath=filepath,
    )
    create_terraform_file(
        filename='variables.tf',
        filepath=filepath,
    )
    create_terraform_file(
        filename='outputs.tf',
        filepath=filepath,
    )

    if add_terraform_docs_config_file:
        create_terraform_docs_config_file(
            filepath=filepath
        )