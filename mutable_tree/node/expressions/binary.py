from enum import Enum
from ..node import NodeType
from .expression import Expression
from ..utils import is_expression


class BinaryOps(Enum):
    ADD = '+'
    MINUS = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    GT = '>'
    LT = '<'
    GE = '>='
    LE = '<='
    EQ = '=='
    NE = '!='
    AND = '&&'
    OR = '||'
    BITWISE_XOR = '^'
    BITWISE_AND = '&'
    BITWISE_OR = '|'
    MOD = '%'
    LSHIFT = '<<'
    RSHIFT = '>>'
    LRSHIFT = '>>>'


class BinaryExpression(Expression):

    def __init__(self, node_type: NodeType, left: Expression, right: Expression,
                 op: BinaryOps):
        super().__init__(node_type)
        self.left = left
        self.right = right
        self.op = op
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.BINARY_EXPR:
            raise TypeError(f'Invalid type: {self.node_type} for BinaryExpression')
        if not is_expression(self.left):
            raise TypeError(f'Invalid type: {self.left.node_type} for BinOp LHS')
        if not is_expression(self.right):
            raise TypeError(f'Invalid type: {self.right.node_type} for BinOp RHS')

    def to_string(self) -> str:
        return f'{self.left.to_string()} {str(self.op)} {self.right.to_string()}'
