from ..node import Node, NodeType
from .expression import Expression


class InstanceofExpression(Expression):

    def __init__(self, node_type: NodeType, left: Expression, right: Node):
        super().__init__(node_type)
        self.left = left
        self.right = right

    def _check_types(self):
        if self.node_type != NodeType.INSTANCEOF_EXPR:
            raise TypeError(f'Invalid type: {self.node_type} for InstanceofExpression.')

    def to_string(self) -> str:
        return f'{self.left.to_string()} instanceof {self.right.to_string()}'
