from ..node import Node, NodeType
from typing import Union


class Literal(Node):

    def __init__(self, node_type: NodeType, value: Union[str, int, float]):
        super().__init__(node_type)
        self.value = value
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.LITERAL:
            raise TypeError(f'Invalid type: {self.node_type} for Literal')

    def to_string(self) -> str:
        return str(self.value)
