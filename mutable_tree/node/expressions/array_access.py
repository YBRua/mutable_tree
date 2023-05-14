from ..node import NodeType
from .expression import Expression
from ..utils import is_primary_expression, is_expression
from . import PrimaryExpression


class ArrayAccess(Expression):

    def __init__(self, node_type: NodeType, array: PrimaryExpression, index: Expression):
        super().__init__(node_type)
        self.array = array
        self.index = index
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.ARRAY_ACCESS:
            raise TypeError(f'Invalid type: {self.node_type} for ArrayAccess')
        if not is_primary_expression(self.array.node_type):
            raise TypeError(f'Invalid type: {self.array.node_type} for array')
        if not is_expression(self.index.node_type):
            raise TypeError(f'Invalid type: {self.index.node_type} for array index')

    def to_string(self) -> str:
        return f'{self.array.to_string()}[{self.index.to_string()}]'
