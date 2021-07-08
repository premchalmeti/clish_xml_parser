# built-in imports
import os

# third-party imports

# custom imports
import config


class CmdNode:
    """
    CmdNode represents the individual token of a command and leaf nodes contains
    metadata of the complete command

    The cmd_node representation for "network device add" command will be,
            -----------------------
            |  network (root)     |
            |  pure_cmd: ""       |
            |  cmd_token: network |
            -----------------------
                      |
            -----------------------
            |  device             |
            |  pure_cmd: "device" |
            |  cmd_token: device  |
            -----------------------
                     |
            ---------------------------
            |  add                    |
            |  pure_cmd: "device add" |
            |  cmd_token: add         |
            |    meta: {              |
            |    'safe': <bool>       |
            |      ...                |
            |    }                    |
            ---------------------------

    complete cmd: "network device add"
    cmd_tokens: ["network", "device", "add"]
    pure_cmd: A pure command is used for lookup in the CLISH XML.

    """
    def __init__(self, cmd_token, pure_cmd):
        self.cmd_token = cmd_token
        self.is_leaf_node = False
        self.meta = {}
        self.childs = []
        self.pure_cmd = pure_cmd

        # non-leaf nodes computed based on child nodes visibility
        self.__visible = True

    def get_descedent(self, cmd_token):
        if self.cmd_token == cmd_token: return self

        for c in self.childs:
            node = c.get_descedent(cmd_token)
            if node:
                return node

    def is_child_exists(self, cmd_token):
        return any(cmd_token==c.cmd_token for c in self.childs)

    def append_child(self, cmd_token):
        if self.is_child_exists(cmd_token):
            return

        pure_cmd = f'{self.pure_cmd} {cmd_token}' if self.pure_cmd else cmd_token

        node = CmdNode(cmd_token, pure_cmd)
        self.childs.append(node)
        return node

    @property
    def visible(self):
        if self.is_leaf_node:
            return self.meta.get('safe')
        return self.__visible

    @visible.setter
    def visible(self, v):
        self.__visible = v

    def __str__(self):
        return f"<{self.__class__.__name__}({self.cmd_token})>"

    __repr__ = __str__


class CmdTree:
    """
    A CmdTree instance represents a tree definition for the clish xml module.
    This tree is a collection of CmdNodes having `root` as starting point.
            -----------------------
            |  network (root)     |
            |  pure_cmd: ""       |
            |  cmd_token: network |
            -----------------------
                      |
            -----------------------
            |  device             |
            |  pure_cmd: "device" |
            |  cmd_token: device  |
            -----------------------
                     |
            ---------------------------
            |  add                    |
            |  pure_cmd: "device add" |
            |  cmd_token: add         |
            |    meta: {              |
            |    'safe': <bool>       |
            |      ...                |
            |    }                    |
            ---------------------------
    """
    def __init__(self, clish_xml_name, clish_xml_path, root=None):
        self.root = root
        self.clish_xml_name = clish_xml_name
        self.clish_xml_path = os.path.join(
            config.SOURCE_XML_DIR, clish_xml_path
        )

    def set_root(self, token):
        self.root = CmdNode(token, '')

    def append_cmd_node(self, parent, child):
        if not self.root:
            self.set_root(parent)

        parent_node_obj = self.root.get_descedent(parent)
        return parent_node_obj.append_child(child)

    def add_cmd(self, cmd, meta):
        tokens = cmd.split(' ')
        N = len(tokens)

        cur_node = None

        for i in range(N-1):
            cur_node = self.append_cmd_node(parent=tokens[i], child=tokens[i+1])

        cur_node.complete_cmd = cmd
        cur_node.meta = meta
        cur_node.is_leaf_node = True

    def __str__(self):
        return f"<{self.__class__.__name__}({self.root})>"

    __repr__ = __str__


if __name__ == '__main__':
    ct = CmdTree('network', 'network.xml')

    cmds = [
        {
            "cmd": "network show",
            "meta": {
                "safe": True
            }
        },
        {
            "cmd": "network device add", 
            "meta": {
                "safe": False
            }
        },
        {
            "cmd": "network device delete", 
            "meta": {
                "safe": False
            }
        }
    ]

    for cmd_node in cmds:
        cmd = cmd_node['cmd']
        meta = cmd_node['meta']

        ct.add_cmd(cmd, meta)
