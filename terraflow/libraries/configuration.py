from dataclasses import dataclass, field


@dataclass
class Configuration:
    add_inline_descriptions: bool = False
    add_header_terraform_docs_url: bool = False
    header_comment: str = ""
    required_attributes_only: bool = False
    required_blocks_only: bool = False
    exclude_attributes: list = field(default_factory=list)
    exclude_computed_attributes: bool = True
    exclude_blocks: list = field(default_factory=list)
    exclude_computed_blocks: bool = True
    attribute_defaults: dict = field(default_factory=dict)
    attribute_value_prefix: str = ""
    auto_create_variables: bool = True


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
class VariableConfiguration:
    # TODO: It could be helpful to add things like add-description or add-type
    pass


@dataclass
class OutputConfiguration:
    pass
