import os
import json
import subprocess
import traceback

from terraflow.terraflow.libraries.constants import *
from terraflow.terraflow.libraries.helpers import *


class Schema:
    def __init__(self, filename: str = '.terraflow/schema.json', cache: bool = True, refresh: bool = False):
        self.filename = filename
        self.cache = cache
        self.refresh = refresh
        self.schema = self.get_schema()

    def get_schema(self):
        if not os.path.exists(TERRAFLOW_DIR):
            os.makedirs(TERRAFLOW_DIR)

        if self.filename and os.path.exists(self.filename) and not self.refresh:
            schema = read_json_file(self.filename)
            print(f'\n{colors("OK_BLUE")}Info:{colors()} Reading provider schema from cache.\n')
        else:
            schema = self.fetch_schema()
            self.cache_schema(schema=schema)
            print(f'\n{colors("OK_GREEN")}Success:{colors()} Schema downloaded successfully.\n')

        return schema

    def fetch_schema(self):
        try:
            p = subprocess.run(["terraform", "init"], capture_output=True, text=True)
            return json.loads(subprocess.check_output(["terraform", "providers", "schema", "-json"]).decode("utf-8"))
        except subprocess.CalledProcessError:
            print(
                f'\n{colors(color="WARNING")}Warning:{colors()} The provider versions for this configuration have changed. Running an upgrade.\n'
            )
            p = subprocess.run(["terraform", "init", "-upgrade"], capture_output=True, text=True)
            return json.loads(subprocess.check_output(["terraform", "providers", "schema", "-json"]).decode("utf-8"))

    def cache_schema(self, schema=None):
        _, ext = os.path.splitext(self.filename)
        if ext.lower() != ".json":
            print(f'\n{colors("FAIL")}Error:{colors()} {self.filename} is not a JSON file.\n')
            return

        dirname = os.path.dirname(self.filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        try:
            if schema is None:
                schema = self.get_schema(filename=self.filename, refresh=True)
            write_json_file(self.filename, schema)
            print(f'\n{colors("OK_GREEN")}Success:{colors()} Schema downloaded successfully.\n')
        except Exception as e:
            print(f'\n{colors("FAIL")}Error:{colors()} An error occurred while caching the schema: {traceback.format_exc()}\n')

    def get_provider_schema(self, namespace, provider):
        return self.schema["provider_schemas"][f"{TERRAFORM_REGISTRY_BASE}/{namespace}/{provider}"]["provider"]

    def get_resource_schema(self, namespace, provider, resource):
        if resource and provider not in resource:
            resource = f"{provider}_{resource}"

        return self.schema["provider_schemas"][f"{TERRAFORM_REGISTRY_BASE}/{namespace}/{provider}"]["resource_schemas"][resource]

    def get_data_schema(self, namespace, provider, data_source):
        if data_source and provider not in data_source:
            data_source = f"{provider}_{data_source}"

        return self.schema["provider_schemas"][f"{TERRAFORM_REGISTRY_BASE}/{namespace}/{provider}"]["data_source_schemas"][data_source]

    def get_attribute_schema(self, resource_schema, blocks=None, attribute=None):
        try:
            if blocks:
                for block in blocks:
                    resource_schema = resource_schema["block"]["block_types"].get(block, None)

            return resource_schema["block"]["attributes"].get(attribute, None)
        except Exception:
            print(f'Error while trying to get the attribute schema: {traceback.format_exc()}')

# schema = Schema(refresh=True)
# print(schema.schema)