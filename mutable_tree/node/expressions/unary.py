from enum import Enum
from ..node import NodeType
from .expression import Expression


class UnaryOps(Enum):
    PLUS = '+'
    NEG = '-'
    NOT = '!'
    BITWISE_NOT = '~'


class UnaryExpression(Expression):

    def __init__(self, node_type: NodeType, operand: Expression, op: UnaryOps):
        super().__init__(node_type)
        self.operand = operand
        self.op = op

    def _check_types(self):
        if self.node_type != NodeType.UNARY_EXPR:
            raise TypeError(f'Invalid type: {self.node_type} for UnaryExpression.')

    def to_string(self) -> str:
        return f'{str(self.op)} {self.operand.to_string()}'
