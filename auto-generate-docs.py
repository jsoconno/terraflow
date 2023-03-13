import re

import click

from terraflow import terraflow

# Make sure file exists and is empty
open("docs.md", "w+").close()


def auto_generate_docs(cmd=terraflow, parent=None):
    ctx = click.core.Context(cmd, info_name=cmd.name, parent=parent)

    with open("docs.md") as file:
        text = file.read()

    with open("docs.md", "a") as file:
        text = f"{cmd.get_help(ctx)}\n"
        pattern = "Usage: ((.+?) \[OPTIONS].*)(?:...)?\s*((?:.|\n)*?^$)\n*Options:\n((?:.|\n)*?^$)\n*(?:Commands:\n*((?:.|\n)*))?"
        title = re.search(pattern, text, re.MULTILINE).group(2)
        usage = re.search(pattern, text, re.MULTILINE).group(1)
        description = re.search(pattern, text, re.MULTILINE).group(3).replace("\n", " ")
        options = re.search(pattern, text, re.MULTILINE).group(4)
        commands = str(re.search(pattern, text, re.MULTILINE).group(5))
        print(usage)
        file.write(f"# {title}\n")
        file.write(f"{description}\n")
        file.write("## Usage\n")
        file.write(f"```\n{usage}\n```\n")
        file.write("## Options\n")
        file.write(f"```\n{options.rstrip()}\n```\n")
        file.write("## Commands\n")
        file.write(f"```\n{commands.rstrip()}\n```\n")
        file.write("## CLI Help\n")
        file.write(f"```\n{text.rstrip()}\n```\n")
        file.write("\n")

    commands = getattr(cmd, "commands", {})
    for sub in commands.values():
        auto_generate_docs(sub, ctx)


if __name__ == "__main__":
    auto_generate_docs()