from ..node import Node, NodeType


class TypeIdentifier(Node):

    def __init__(self, node_type: NodeType, value: str):
        super().__init__(node_type)
        self.value = value

    def _check_types(self):
        if self.node_type != NodeType.TYPE_IDENTIFIER:
            raise TypeError(f'Invalid type: {self.node_type} for TypeIdentifier.')

    def to_string(self) -> str:
        return self.value
