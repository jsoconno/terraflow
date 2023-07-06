from dataclasses import dataclass, field

@dataclass
class Configuration:
    add_inline_descriptions: bool = False
    add_header_terraform_docs_url: bool = False
    header_comment: str = ''
    required_attributes_only: bool = False
    required_blocks_only: bool = False
    exclude_attributes: list = field(default_factory=list)
    exclude_computed_attributes: bool = True
    exclude_blocks: list = field(default_factory=list)
    exclude_computed_blocks: bool = True
    attribute_defaults: dict = field(default_factory=dict)
    attribute_value_prefix: str = ""

@dataclass
class ProviderConfiguration(Configuration):
    pass

@dataclass
class ResourceConfiguration(Configuration):
    pass

@dataclass
class DataSourceConfiguration(Configuration):
    pass

@dataclass
class VariableConfiguration(Configuration):
    include_variables: list = field(default_factory=list)

@dataclass
class OutputConfiguration(Configuration):
    include_outputs: list = field(default_factory=list)
