# built-in imports
import os

# third-party imports

# custom imports

# source xml location to be used for parsing and creating safe xmls
SOURCE_XML_DIR = 'source_xmls'

# safe xmls will be written to `OUTPUT_XML_DIR`
OUTPUT_XML_DIR = 'target_xmls'

# schema file to be used by schema manager to prepare cmd tree
SCHEMA_DIR = 'schema'
SCHEMA_FILE = os.path.join(SCHEMA_DIR, 'network_schema.json')
