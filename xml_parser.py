# built-in imports
import os

# third-party imports

# custom imports
import config
import xml.etree.ElementTree as ET


XML_BASE_SCHEMA = "http://clish.sourceforge.net/XMLSchema"


class XMLParser:
    """
    The XMLParser contains all the utility functions related to parsing the
    CLISH XML
    """

    def __init__(self, xml):
        self.xml_tree = self.load_xml(xml)
        self.xml_root = self.xml_tree.getroot()

    def load_xml(self, xml):
        return ET.parse(xml)

    def get_cmd_node(self, cmd):
        cmd_nodes = self.xml_root.findall(
            ".//{%s}COMMAND[@name='%s']" % (
                XML_BASE_SCHEMA, cmd
            )
        )

        if not cmd_nodes:
            print(f"===> No matching {cmd} cmd found")
            return

        xml_cmd_node = cmd_nodes[0]

        return xml_cmd_node

    def remove_cmd(self, cmd):
        xml_cmd_node = self.get_cmd_node(cmd)

        if xml_cmd_node is not None:
            self.xml_root.remove(xml_cmd_node)
            return True

        return False

    def output_xml(self):
        ET.register_namespace('', XML_BASE_SCHEMA)

        file = os.path.basename(self.cmd_tree.clish_xml_path)
        self.xml_tree.write(
            os.path.join(config.OUTPUT_XML_DIR, file),
            encoding='utf-8',
            xml_declaration=True
        )
