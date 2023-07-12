def format_comments(comments):
    if comments:
        formatted_comments = "\n".join([f"# {comment}" for comment in comments])
        return f"{formatted_comments}\n"
    else:
        return ""

def wrap_text(text, line_length=80, prefix=''):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + word) + 1 <= line_length:
            if current_line:
                current_line += " "
            current_line += word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    # Adding prefix to each line
    lines = [f"{prefix} {line}".strip() for line in lines]

    return lines

def format_list(items: list, title: str = None, top: int = None, prefix: str = " - ") -> str:
    """
    Format a list for output in the terminal.

    Args:
        items: The list of items to format.
        title: The optional title for the formatted list.
        top: The optional maximum number of items to include.
        prefix: The prefix string to prepend to each item.

    Returns:
        The formatted list as a string.
    """
    formatted_list = "\n"

    if title:
        formatted_list += f"{title}\n\n"

    if top:
        items = items[:top]

    for option in items:
        formatted_list += f"{prefix}{option}\n"

    return formatted_list

def colors(color: str = "END") -> str:
    """
    Returns ANSI color codes for printing to the command line.

    Args:
        color: The color name to retrieve the code for.

    Returns:
        The ANSI color code as a string.
    """
    colors = {
        "HEADER": "\033[95m",
        "OK_BLUE": "\033[94m",
        "OK_CYAN": "\033[96m",
        "OK_GREEN": "\033[92m",
        "WARNING": "\033[93m",
        "FAIL": "\033[91m",
        "END": "\033[0m",
        "BOLD": "\033[1m",
        "UNDERLINE": "\033[4m",
    }

    return colors[color]

def format_resource_header(type, name, provider=None, kind=None, documentation_url=None, comment=None):
    header_content = ""

    if documentation_url:
        header_content += f"# Terraform docs: {documentation_url}\n"

    if comment:
        wrapped_comment = "\n".join(["# " + line for line in wrap_text(text=comment)])
        header_content += f"{wrapped_comment}\n"

    if type == 'provider':
        header = f'{type} "{name}" {{'
    else:
        header = f'{type} "{provider}_{kind}" "{name}" {{'
    header_content += f"{header}\n"
    footer = "}\n"

    return header_content, footer

def format_block_header(schema, block, block_hierarchy):
    header = ""
    if schema.get("min_items", 0) > 0:
        required_blocks_message = "required"
    else:
        required_blocks_message = "optional"

    header += f"\n# This block is {required_blocks_message}\n"
    header += f"{block} {{\n"
    footer = "}\n"

    return header, footer

def format_attribute(attribute: str, attribute_schema: dict, attribute_description: str = None, block_hierarchy: list = [], configuration: object = None):
    # Join block hierarchy and attribute with '_'
    hierarchy_key = "_".join(block_hierarchy + [attribute])

    # If hierarchy_key exists in attribute_defaults dictionary, set attribute_value accordingly
    if hierarchy_key in configuration.attribute_defaults:
        attribute_value = configuration.attribute_defaults[hierarchy_key]
    elif configuration.attribute_value_prefix:  # If attribute_value_prefix is given
        attribute_value = f'var.{configuration.attribute_value_prefix}_{hierarchy_key}'
    else:
        attribute_value = f'var.{hierarchy_key}'
    
    # Check if attribute value starts with the provided prefixes
    prefixes = ("var.", "local.", "resource.", "data.", "module.", "{", "[")
    if not attribute_value.startswith(prefixes):
        attribute_value = f'"{attribute_value}"'
    
    # Construct the attribute line
    if configuration.add_inline_descriptions and attribute_description:
        attribute_line = f'{attribute} = {attribute_value} # {attribute_description}' + '\n'
    else:
        attribute_line = f'{attribute} = {attribute_value}'+ '\n'
    
    return attribute_line


def format_attribute_type(attribute_type):
    """
    Formats the attribute type from the provider schema for use in variables.
    """
    if isinstance(attribute_type, str):
        return attribute_type
    elif isinstance(attribute_type, list):
        element_type = format_attribute_type(attribute_type[-1])
        for i in range(len(attribute_type) - 2, -1, -1):
            element_type = f"{attribute_type[i]}({element_type})"
        return element_type
    elif isinstance(attribute_type, dict):
        object_type = "{\n"
        for key, value in attribute_type.items():
            object_type += f"{key} = {format_attribute_type(value)}\n"
        object_type += "}"
        return object_type
    else:
        raise ValueError(f"Invalid Terraform data type: {attribute_type}")

def format_terraform_code(code: str, indentation='  '):
    """
    Indent Terraform code so that it is formatted correctly.

    Args:
        code (str): The Terraform code to format.
        indentation (str): The string used for each level of indentation. Defaults to two spaces.
    """

    # Split the code into lines
    lines = code.split('\n')

    # Initialize a counter for the current level of indentation
    indent_level = 0

    # Process each line
    for i, line in enumerate(lines):
        # Increase the indent level if the line opens a block
        if '{' in line and '}' not in line:
            lines[i] = indent_level * indentation + line.lstrip()
            indent_level += 1
        # Decrease the indent level if the line closes a block
        elif '}' in line and '{' not in line:
            indent_level -= 1
            lines[i] = indent_level * indentation + line.lstrip()
        # No change in indent level if the line both opens and closes a block
        elif '{' in line and '}' in line:
            lines[i] = indent_level * indentation + line.lstrip()
        # Otherwise, just add the current level of indentation
        else:
            lines[i] = indent_level * indentation + line.lstrip()

    # Join the lines back together and return the result
    return '\n'.join(lines)
