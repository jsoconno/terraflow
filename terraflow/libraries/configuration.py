from dataclasses import dataclass, field

@dataclass
class Configuration:
    add_descriptions: bool = False
    required_attributes_only: bool = False
    required_blocks_only: bool = False
    exclude_blocks: list = field(default_factory=list)
    exclude_attributes: list = field(default_factory=list)
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
