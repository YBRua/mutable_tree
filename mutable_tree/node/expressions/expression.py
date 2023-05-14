from ..node import Node, NodeType


class Expression(Node):

    def __init__(self, node_type: NodeType):
        super().__init__(node_type)
