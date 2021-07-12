# built-in imports
import json

# third-party imports

# custom imports
import config
from cmd_tree import CmdTree


class SchemaManager:
    """
    SchemaManager reads the json file which contains the CLISH commands schema
    and meta data used while parsing the CLISH XML.
    The SchemaManager prepares an instance of CmdTree which contains all the 
    definition of a module to be used while parsing the CLISH XML
    """
    def __init__(self, schema_file):
        self.schema_file = schema_file
        self.schema_json = self.read_schema()

    def read_schema(self):
        with open(self.schema_file) as fd:
            return json.load(fd)

    def get_module(self):
        return self.schema_json['module']

    def get_cmds(self):
        module = self.get_module()
        return module['commands']

    def prepare_cmd_tree(self):
        modules_json = self.get_module()

        cmd_tree = CmdTree(
            clish_xml_name=modules_json.get('name'), 
            clish_xml_path=modules_json.get('source_file')
        )

        for cmd_node in self.get_cmds():
            cmd_tree.add_cmd(cmd_node['cmd'], cmd_node['meta'])

        return cmd_tree


if __name__ == '__main__':
    schema_mgr = SchemaManager(config.SCHEMA_FILE)
    cmd_tree = schema_mgr.prepare_cmd_tree()

    from clish_parser import CLISHParser

    cp = CLISHParser(cmd_tree)
    cp.parse_cmd_tree()
    cp.output_xml()
