# built-in imports
import os

# third-party imports

# custom imports
import config
import xml.etree.ElementTree as ET


XML_BASE_SCHEMA = "http://clish.sourceforge.net/XMLSchema"


class XMLParser:
    """
    The XmlParser contains all the utility functions related to parsing the
    CLISH XML
    """

    def __init__(self, xml):
        self.xml_root = self.load_xml(xml)
        self.view_node = self.load_view_node()

    def load_xml(self, xml):
        return ET.parse(xml)

    def load_view_node(self):
        matched_nodes = self.xml_root.findall(
            './/{%s}VIEW' % XML_BASE_SCHEMA
        )
        if len(matched_nodes) == 0:
            raise Exception(f"No matching VIEW tag found")

        return matched_nodes[0]

    def get_cmd_node_from_view_node(self, cmd):
        cmd_nodes = self.view_node.findall(
            ".//{%s}COMMAND[@name='%s']" % (
                XML_BASE_SCHEMA, cmd
            )
        )

        if not cmd_nodes:
            print(f"===> No matching {cmd} cmd found")
            return

        xml_cmd_node = cmd_nodes[0]

        return xml_cmd_node

    def generate_target_xml(self):
        ET.register_namespace('', XML_BASE_SCHEMA)

        file = os.path.basename(self.cmd_tree.clish_xml_path)
        self.xml_root.write(
            os.path.join(config.OUTPUT_XML_DIR, file),
            encoding='utf-8',
            xml_declaration=True
        )
