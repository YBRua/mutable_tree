from ..node import Node, NodeType


class ThisExpression(Node):

    def __init__(self, node_type: NodeType):
        super().__init__(node_type)
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.THIS_EXPR:
            raise TypeError(f'Invalid type: {self.node_type} for ThisExpression')

    def to_string(self) -> str:
        return 'this'