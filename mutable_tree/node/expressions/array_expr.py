from ..node import NodeType
from .expression import Expression
from .expression import is_expression
from typing import List


class ArrayExpression(Expression):

    def __init__(self, node_type: NodeType, elements: List[Expression]):
        super().__init__(node_type)
        self.elements = elements
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.ARRAY_EXPR:
            raise TypeError(f'Invalid type: {self.node_type} for ArrayExpression')
        for i, elem in enumerate(self.elements):
            if not is_expression(elem):
                raise TypeError(f'Invalid type: {elem.node_type} for array element {i}')

    def to_string(self) -> str:
        return f'{{{", ".join(elem.to_string() for elem in self.elements)}}}'
