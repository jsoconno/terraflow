import os
import re
import json
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from typing import List, Tuple, Optional
import difflib

from terraflow.libraries.constants import *

# File and folder manipulation functions.

def read_text_file(filename: str) -> str:
    """
    Read the contents of a text file.

    Args:
        filename: The name of the file to read.

    Returns:
        The contents of the text file as a string.
    """
    with open(filename, "r") as file:
        return file.read()

def write_text_file(filename: str, content: str) -> None:
    """
    Write content to a text file.

    Args:
        filename: The name of the file to write.
        content: The content to be written.
    """
    with open(filename, "w") as file:
        file.write(content)

def read_json_file(filename: str) -> dict:
    """
    Reads JSON from a file.

    Args:
        filename: The name of the file to read.

    Returns:
        A dictionary representing the JSON data.
    """
    with open(filename, "r") as json_file:
        return json.loads(json_file.read())

def write_json_file(filename: str, data: dict) -> None:
    """
    Writes data as JSON to a file.

    Args:
        filename: The name of the file to write.
        data: The data to be written as JSON.
    """
    with open(filename, "w") as f:
        json.dump(data, f)

def write_terraform_to_file():
    """
    Write a Terraform provider, resource, data source, variable, or output block to a file based on a regex pattern.
    """
    pass

# Formatting functions.

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

def format_terminal_text():
    """
    Formats text for terminal output.
    """
    pass

# Helper functions

def calculate_levenshtein_distance(s: str, t: str) -> float:
    """
    Calculate the normalized Levenshtein distance between two strings.

    Args:
        s: The first string.
        t: The second string.

    Returns:
        The normalized Levenshtein distance between the two strings as a float.
    """
    # Convert the strings to lowercase
    s = s.lower()
    t = t.lower()

    # Initialize the distance matrix with zeros
    d = [[0 for _ in range(len(t) + 1)] for _ in range(len(s) + 1)]

    # Fill the first row and column of the matrix
    for i in range(len(s) + 1):
        d[i][0] = i
    for j in range(len(t) + 1):
        d[0][j] = j

    # Compute the minimum edit distance
    for j in range(1, len(t) + 1):
        for i in range(1, len(s) + 1):
            if s[i - 1] == t[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1]) + 1

    # Compute the maximum possible distance
    max_distance = max(len(s), len(t))

    # Normalize the distance
    if max_distance == 0:
        normalized_distance = 0.0
    else:
        normalized_distance = d[len(s)][len(t)] / max_distance

    return normalized_distance


def convert_strings_to_dict(text: str, delimiter: str = "=") -> dict:
    """
    Converts a string to a dictionary based on a delimiter.

    Args:
        text: The string to convert.
        delimiter: The delimiter used to split the string (default: "=").

    Returns:
        A dictionary created from the string, where the keys and values are separated by the delimiter.
    """
    dictionary = {}
    for x in text:
        k, v = x.split(delimiter)
        dictionary[k] = v

    return dictionary

def scrape_website(url: str, tag: str = None, selector: str = None, list_output: bool = False) -> str:
    """
    Scrape content from a URL. If a tag or selector is specified, only content within that tag or selector is scraped.

    Args:
        url: The URL to scrape.
        tag: Optional; an HTML tag name to scrape (e.g. "p" for paragraph tags, "div" for div tags, etc.).
        selector: Optional; a CSS selector to scrape.
        list_output: Optional; whether to return the output as a list (default is False).

    Returns:
        The scraped content as a string or a list of strings.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        response.raise_for_status()  # If the response contains an HTTP error status code, raise an exception
    except RequestException as e:
        print(f"Failed to get the webpage. Error: {e}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    if tag:
        elements = soup.find_all(tag)
    elif selector:
        elements = soup.select(selector)
    else:
        return '\n'.join(line.strip() for line in soup.text.split('\n') if line.strip())

    texts = ['\n'.join(line.strip() for line in elem.get_text().split('\n') if line.strip()) for elem in elements]

    if list_output:
        return texts
    else:
        return '\n'.join(texts)

# File and folder manipulation functions.

def read_text_file(filename: str) -> str:
    """
    Read the contents of a text file.

    Args:
        filename: The name of the file to read.

    Returns:
        The contents of the text file as a string.
    """
    with open(filename, "r") as file:
        return file.read()

def write_text_file(filename: str, content: str) -> None:
    """
    Write content to a text file.

    Args:
        filename: The name of the file to write.
        content: The content to be written.
    """
    with open(filename, "w") as file:
        file.write(content)

def read_json_file(filename: str) -> dict:
    """
    Reads JSON from a file.

    Args:
        filename: The name of the file to read.

    Returns:
        A dictionary representing the JSON data.
    """
    with open(filename, "r") as json_file:
        return json.loads(json_file.read())

def write_json_file(filename: str, data: dict) -> None:
    """
    Writes data as JSON to a file.

    Args:
        filename: The name of the file to write.
        data: The data to be written as JSON.
    """
    with open(filename, "w") as f:
        json.dump(data, f)

def write_terraform_to_file():
    """
    Write a Terraform provider, resource, data source, variable, or output block to a file based on a regex pattern.
    """
    pass

# Formatting functions.

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

def format_terminal_text():
    """
    Formats text for terminal output.
    """
    pass

# Helper functions

def calculate_levenshtein_distance(s: str, t: str) -> float:
    """
    Calculate the normalized Levenshtein distance between two strings.

    Args:
        s: The first string.
        t: The second string.

    Returns:
        The normalized Levenshtein distance between the two strings as a float.
    """
    # Convert the strings to lowercase
    s = s.lower()
    t = t.lower()

    # Initialize the distance matrix with zeros
    d = [[0 for _ in range(len(t) + 1)] for _ in range(len(s) + 1)]

    # Fill the first row and column of the matrix
    for i in range(len(s) + 1):
        d[i][0] = i
    for j in range(len(t) + 1):
        d[0][j] = j

    # Compute the minimum edit distance
    for j in range(1, len(t) + 1):
        for i in range(1, len(s) + 1):
            if s[i - 1] == t[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1]) + 1

    # Compute the maximum possible distance
    max_distance = max(len(s), len(t))

    # Normalize the distance
    if max_distance == 0:
        normalized_distance = 0.0
    else:
        normalized_distance = d[len(s)][len(t)] / max_distance

    return normalized_distance


def convert_strings_to_dict(text: str, delimiter: str = "=") -> dict:
    """
    Converts a string to a dictionary based on a delimiter.

    Args:
        text: The string to convert.
        delimiter: The delimiter used to split the string (default: "=").

    Returns:
        A dictionary created from the string, where the keys and values are separated by the delimiter.
    """
    dictionary = {}
    for x in text:
        k, v = x.split(delimiter)
        dictionary[k] = v

    return dictionary


def is_valid_version(version: str, valid_versions: list) -> bool:
    """
    Checks whether a provided version is valid based on a given list.

    Args:
        version: The version to validate.
        valid_versions: A list of valid versions.

    Returns:
        True if the version is valid, False otherwise.
    """
    return version in valid_versions

def scrape_website(url: str, tag: str = None, selector: str = None, list_output: bool = False) -> str:
    """
    Scrape content from a URL. If a tag or selector is specified, only content within that tag or selector is scraped.

    Args:
        url: The URL to scrape.
        tag: Optional; an HTML tag name to scrape (e.g. "p" for paragraph tags, "div" for div tags, etc.).
        selector: Optional; a CSS selector to scrape.
        list_output: Optional; whether to return the output as a list (default is False).

    Returns:
        The scraped content as a string or a list of strings.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        response.raise_for_status()  # If the response contains an HTTP error status code, raise an exception
    except RequestException as e:
        print(f"Failed to get the webpage. Error: {e}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    if tag:
        elements = soup.find_all(tag)
    elif selector:
        elements = soup.select(selector)
    else:
        return '\n'.join(line.strip() for line in soup.text.split('\n') if line.strip())

    texts = ['\n'.join(line.strip() for line in elem.get_text().split('\n') if line.strip()) for elem in elements]

    if list_output:
        return texts
    else:
        return '\n'.join(texts)

# Documentation functions.

def get_terraform_documentation_url(namespace: str, provider: str, resource: str, scope: str, version: str = 'main') -> str:
    """
    Get the documentation URL for a provider resource or data source.

    Args:
        namespace: The namespace of the provider.
        provider: The provider name.
        resource: The resource or data source name.
        scope: The scope of the documentation (resource or data source).
        version: The version of the provider (default: 'main').

    Returns:
        The documentation URL as a string.
    """
    url = f"https://registry.terraform.io/v1/providers/{namespace}/{provider}"
    response = json.loads(requests.get(url).text)

    docs_path = None

    for doc in response["docs"]:
        if (
            doc["title"] == resource
            or doc["title"] == resource.replace(f"{provider}_", "")
        ) and doc["category"] == f"{scope.replace('_', '-')}s":
            docs_path = doc["path"]

    if docs_path:
        if scope == "provider":
            url = f"https://github.com/{namespace}/terraform-provider-{provider}"
        else:
            # TODO: replace "main" with the actual version of the provider from the configuration.
            url = f"https://github.com/{namespace}/terraform-provider-{provider}/blob/{version}/{docs_path}"
    else:
        url = None

    return url

def get_terraform_documentation(namespace: str, provider: str, scope: str, resource: str, version: str = 'main', cache: bool = True) -> str:
    """
    Get the documentation for a provider resource or data source and cache it.

    Args:
        namespace: The namespace of the provider.
        provider: The provider name.
        scope: The scope of the documentation (resource or data source).
        resource: The resource or data source name.
        version: The version of the provider (default: 'main').
        cache: Whether to cache the documentation (default: True).

    Returns:
        The documentation content as a string.
    """
    # Determine the filename for the cached documentation
    filename = f"{namespace}.{provider}.{resource}.{scope}.txt"
    path = os.path.join(DOCUMENTATION_DIR, filename)

    # If the file exists, read the cached documentation
    if os.path.exists(path):
        print(f'\n{colors("OK_BLUE")}Info:{colors()} Reading documentation from cache.\n')
        return read_text_file(path)

    # If the file does not exist, get the documentation URL and the documentation
    documentation_url = get_terraform_documentation_url(namespace, provider, resource, scope, version)
    documentation = scrape_website(documentation_url, tag="article")

    # If caching is enabled, cache the documentation
    if cache:
        try:
            if not os.path.exists(DOCUMENTATION_DIR):
                os.makedirs(DOCUMENTATION_DIR)

            write_text_file(path, documentation)

            print(f'\n{colors("OK_GREEN")}Success:{colors()} Documentation read and cached successfully.\n')
        except Exception:
            print(f'\n{colors("FAIL")}Error:{colors()} An error occurred while caching the documentation.\n')

    return documentation

def get_resource_attribute_description(
    documentation_text, attribute, block_hierarchy=None
):
    # Extract the attribute descriptions from the text
    pattern = rf"(^{attribute})\s+-\s+(.*)"
    attribute_matches = re.findall(
        pattern=pattern, string=documentation_text, flags=re.MULTILINE
    )
    attribute_matches = [str(x[1]) for x in attribute_matches]

    # if there is more than one match on an attribute name
    if len(attribute_matches) > 1:
        # Check is there is a list of blocks
        if block_hierarchy:
            # Then for each match rank them based on a normalized distance algorithm
            levenshtein_distances = []
            for match in attribute_matches:
                normalized_block_text = " ".join(block_hierarchy).replace("_", " ")
                # Calculate the normalized distance
                normalized_distance = calculate_levenshtein_distance(match, normalized_block_text)
                current_block = block_hierarchy[-1]
                # If the current block name is in the match
                if current_block in match:
                    # Add a multiplier if the exact block name is in the string
                    normalized_distance = normalized_distance - 0.1
                else:
                    # For each key word in the block list
                    for keyword in block_hierarchy:
                        # Go through each word in the description text
                        for word in match.split(" "):
                            # Calculate a similarity score
                            similarity_score = difflib.SequenceMatcher(
                                None, keyword.lower().replace("_", " "), word.lower()
                            ).ratio()
                            # And if that score is below a threshold, add another multiplier
                            if similarity_score > 0.8:
                                # print(f'{keyword} -> {word} = score: {similarity_score}')
                                normalized_distance = normalized_distance - 0.1
                        # elif word
                # Create a list of scores
                levenshtein_distances.append(normalized_distance)

            # Sort and get the lowest scoring description
            levenshtein_distances, descriptions = zip(
                *sorted(zip(levenshtein_distances, attribute_matches))
            )

            # Select the description with the lowest distance
            description = descriptions[0]

            # print(levenshtein_distances)
            # print(descriptions)
        else:
            # Take the first item found
            description = attribute_matches[0]
    elif len(attribute_matches) == 1:
        description = attribute_matches[0]
    else:
        description = ""

    return description

# namespace = "hashicorp"
# provider = "azurerm"
# resource = "key_vault"
# scope = "resource"

# get_terraform_documentation(namespace, provider, scope, resource, cache=True)

# Version functions.

def get_semantic_version(version: str) -> Optional[Tuple[int, int, int, int]]:
    """
    Get a tuple representing the semantic version components including major, minor, patch, and pre-release.

    Args:
        version (str): The version string.

    Returns:
        Optional[Tuple[int, int, int, int]]: A tuple containing the version components or None if the version is invalid.
    """
    regex_pattern = r'(\d+)\.*(\d+)*\.*(\d+)*(?:-*(?:(?:[a-zA-Z]*(\d*)))?)'

    try:
        match = re.match(regex_pattern, version)
        if match:
            version_components = match.groups()
            version_components = tuple(int(component) if component is not None else 0 for component in version_components)
            version_length = len(version_components)
            missing_version_components = 4 - version_length

            if missing_version_components > 0:
                # Adding the version length at the end is used for pessimistic constraint operator logic.
                version_components += (0,) * (missing_version_components - 1) + (1000000000000000,) + (version_length,)

            return version_components
    except Exception:
        pass

    return None

def sort_versions(versions: List[str], reverse: bool = True) -> List[str]:
    """
    Sorts lists of versions based on the semantic version.

    Args:
        versions (List[str]): The list of versions to sort.
        reverse (bool, optional): Determines whether to sort in ascending (False) or descending (True) order.
                                  Defaults to True.

    Returns:
        List[str]: The sorted list of versions.
    """
    tuple_versions = [get_semantic_version(version) for version in versions]
    versions = [x for _, x in sorted(zip(tuple_versions, versions), reverse=reverse)]
    return versions

def is_valid_version(version: str, valid_versions: list) -> bool:
    """
    Checks whether a provided version is valid based on a given list.

    Args:
        version: The version to validate.
        valid_versions: A list of valid versions.

    Returns:
        True if the version is valid, False otherwise.
    """
    return version in valid_versions

# versions = ["1.0.0", "1.1.0", "0.1.3", "0.1.1-alpha", "2.0.0"]
# print(sort_versions(versions))
