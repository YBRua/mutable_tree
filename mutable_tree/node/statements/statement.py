from ..node import Node, NodeType


class Statement(Node):

    def __init__(self, node_type: NodeType):
        super().__init__(node_type)
