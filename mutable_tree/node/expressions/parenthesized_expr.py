from ..node import NodeType
from .expression import Expression
from .expression import is_expression


class ParenthesizedExpression(Expression):

    def __init__(self, node_type: NodeType, expr: Expression):
        super().__init__(node_type)
        self.expr = expr
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.PARENTHESIZED_EXPR:
            raise TypeError(
                f'Invalid type: {self.node_type} for ParenthesizedExpression')
        if not is_expression(self.expr):
            raise TypeError(
                f'Invalid type: {self.expr.node_type} for parenthesized expr')

    def to_string(self) -> str:
        return f'({self.expr.to_string()})'
