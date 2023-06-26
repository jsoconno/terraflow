def colors(color="END"):
    """
    A standard set of colors used for printing to command line.
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

def pretty_list(items=[], title=None, top=None, item_prefix=" - "):
    """
    Implements logic to make output to CLI more clean and consistent.
    """
    pretty_list = "\n"

    if isinstance(items, str):
        items = [items]

    if len(items) > 1:
        item_prefix = item_prefix
    else:
        item_prefix = ""

    if title:
        pretty_list += f"{title}\n\n"

    if top:
        items = items[:top]

    for option in items:
        pretty_list += f"{item_prefix}{option}\n"

    return pretty_list