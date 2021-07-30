# built-in imports

# third-party imports

# custom imports
from xml_parser import XMLParser


class CLISHParser(XMLParser):
    """
    CLISHParser takes a CmdTree which contains all the details of a CLISH 
    XML. 
    CLISHParser traverse the CmdTree and inherits XMLParser to parse the
    given Clish xml.

    """
    def __init__(self, cmd_tree):
        super().__init__(cmd_tree.clish_xml_path)
        self.cmd_tree = cmd_tree

    def action_node(self, node):
        if not node.visible:
            self.remove_cmd(node.cmd)

    def process_node(self, node):
        if not node.is_leaf_node:
            # if not a leaf node process childs first then action current
            for child in node.childs:
                self.process_node(child)

            node.visible = any([child.visible for child in node.childs])

        # the root node doesnt exist in xml
        if node is self.cmd_tree.root:
            return

        self.action_node(node)

    def parse_cmd_tree(self):
        self.process_node(self.cmd_tree.root)

    def output_xml(self):
        if self.cmd_tree.root.visible:
            super().output_xml()


if __name__ == '__main__':
    import config
    from schema_mgr import SchemaManager

    schema_mgr = SchemaManager(config.SCHEMA_FILE)
    cmd_tree = schema_mgr.prepare_cmd_tree()

    cp = CLISHParser(cmd_tree)
    cp.parse_cmd_tree()
    cp.output_xml()
