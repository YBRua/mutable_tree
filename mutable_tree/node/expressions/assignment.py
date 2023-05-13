from enum import Enum
from ..node import Node, NodeType
from .expression import Expression
from ..utils import is_expression


class AssignmentOps(Enum):
    EQUAL = '='
    PLUS_EQUAL = '+='
    MINUS_EQUAL = '-='
    MULTIPLY_EQUAL = '*='
    DIVIDE_EQUAL = '/='
    AND_EQUAL = '&='
    OR_EQUAL = '|='
    XOR_EQUAL = '^='
    MOD_EQUAL = '%='
    LSHIFT_EQUAL = '<<='
    ARSHIFT_EQUAL = '>>='
    LRSHIFT_EQUAL = '>>>='


class AssignmentExpression(Expression):

    def __init__(self, node_type: NodeType, left: Node, right: Expression,
                 op: AssignmentOps):
        super().__init__(node_type)
        self.left = left
        self.right = right
        self.op = op

    def _check_types(self):
        if self.node_type != NodeType.ASSIGNMENT_EXPR:
            raise TypeError(f'Invalid type: {self.node_type} for AssignmentExpression.')
        lt = self.left.node_type
        if lt not in {NodeType.IDENTIFIER, NodeType.FIELD_ACCESS, NodeType.ARRAY_ACCESS}:
            raise TypeError(f'Invalid type: {lt} for Assignment LHS.')
        if not is_expression(self.right):
            raise TypeError(f'Invalid type: {self.right.node_type} for Assignment RHS.')

    def to_string(self) -> str:
        return f'{self.left.to_string()} {str(self.op)} {self.right.to_string()}'
