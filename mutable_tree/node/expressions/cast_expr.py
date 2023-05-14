from ..node import NodeType
from .expression import Expression
from ..types import TypeIdentifier
from .expression import is_expression


class CastExpression(Expression):

    def __init__(self, node_type: NodeType, type_identifier: TypeIdentifier,
                 value: Expression):
        super().__init__(node_type)
        self.type = type_identifier
        self.value = value
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.CAST_EXPR:
            raise TypeError(f'Invalid type: {self.node_type} for CastExpression')
        if not is_expression(self.value):
            raise TypeError(f'Invalid type: {self.value.node_type} for Cast value')
        if self.type.node_type != NodeType.TYPE_IDENTIFIER:
            raise TypeError(f'Invalid type: {self.type.node_type} for Cast type')

    def to_string(self) -> str:
        return f'({self.type.to_string()}) {self.value.to_string()}'
