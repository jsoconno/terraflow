# Class Terraform

self.namespace (namespace) # Namespace of the provider, resource, or data
self.provider (provider) # Provider of the provider, resource, or data
self.code ("") # Code as text
self.config ({}) # Configuration as a map

def write_line() # Writes a line to self.code

# Class Block

self.variables ({}) # Map of variable ids to code
self.outputs ({}) # Map of output ids to code
self.variables_text ("") # Variables text
self.outputs_text ("") # Outputs text
self.documentation_url ("") # The documentation url for the resource
self.documentation_text ("") # The documentation text

def add_variable() # Adds a variable to self.variables
def add_output() # Adds an output to self.outputs
def add_attribute() # Formats an attribute string and writes it to self.code
def write_variables_code() # Adds a variable to self.variables_text
def write_outputs_code() # Adds an output to self.outputs_text
def add_block_wrapper() # Formats header and footer text for blocks
def add_resource_wrapper() # Formats header and footer text for resources
def write_code() # Recursive function that writes headers, bodies, and footers
def get_variables() # Writes and returns self.variables_text
def get_outputs() # Writes and returns self.outputs_text

# Class Provider

self.documentation_url ("") # The documentation url for the resource
self.documentation_text ("") # The documentation text

def get_schema() # Returns the provider schema
def write_provider_code() # Writes provider Terraform code to self.code
def get_code() # Sets config, collects schema, writes and returns Terraform

# Class Resource

self.documentation_url ("") # The documentation url for the resource
self.documentation_text ("") # The documentation text
self.resource (resource) # The type of provider resource
self.name (name) # The name of the provider resource

def get_schema() # Returns the resource schema
def write_resource_code() # Writes resource Terraform code to self.code
def get_code() # Sets config, collects schema, writes and returns Terraform

# Class DataSource

self.documentation_url ("") # The documentation url for the data source
self.documentation_text ("") # The documentation text
self.data source (data source) # The type of provider data source
self.name (name) # The name of the provider data source

def get_schema() # Returns the data source schema
def write_resource_code() # Writes data source Terraform code to self.code
def get_code() # Sets config, collects schema, writes and returns Terraform