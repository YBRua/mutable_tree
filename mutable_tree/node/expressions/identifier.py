from ..node import Node, NodeType


class Identifier(Node):

    def __init__(self, node_type: NodeType, name: str):
        super().__init__(node_type)
        self.name = name
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.IDENTIFIER:
            raise TypeError(f'Invalid type: {self.node_type} for Identifier')

    def to_string(self) -> str:
        return str(self.name)
