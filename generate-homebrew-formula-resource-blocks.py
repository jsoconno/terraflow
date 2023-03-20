import requests

def generate_resource_blocks(requirements_file='requirements.txt'):
    pypi_base_url = "https://pypi.org/pypi"

    with open(requirements_file, "r") as file:
        lines = file.readlines()

    resource_blocks = ""

    for line in lines:
        if line.startswith("-e") or line.startswith("#"):
            continue

        pkg_name, version = line.strip().split("==")
        pkg_info_url = f"{pypi_base_url}/{pkg_name}/{version}/json"
        response = requests.get(pkg_info_url)

        if response.status_code == 200:
            pkg_info = response.json()

            # Select the tar.gz distribution URL
            selected_url = None
            for url_info in pkg_info["urls"]:
                if url_info["url"].endswith(".tar.gz"):
                    selected_url = url_info
                    break

            if selected_url:
                download_url = selected_url["url"]
                sha256 = selected_url["digests"]["sha256"]

                resource_block = f'resource "{pkg_name}" do\n'
                resource_block += f'  url "{download_url}"\n'
                resource_block += f'  sha256 "{sha256}"\n'
                resource_block += "end\n\n"

                resource_blocks += resource_block

    return resource_blocks

if __name__ == "__main__":
    resources_text = generate_resource_blocks()
    print(resources_text)
