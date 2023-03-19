import os
import subprocess
import yaml

from terraflow.libraries.core import colors


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


def create_terraform_docs_config_file(config_filename, sort_by="name"):
    config = {
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

    if not os.path.exists(config_filename):
        with open(config_filename, "w") as file:
            yaml.dump(config, file)


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
