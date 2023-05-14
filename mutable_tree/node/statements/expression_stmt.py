from ..node import NodeType
from .statement import Statement
from ..expressions import Expression
from ..expressions import is_expression


class ExpressionStatement(Statement):

    def __init__(self, node_type: NodeType, expr: Expression):
        super().__init__(node_type)
        self.expr = expr
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.EXPRESSION_STMT:
            raise TypeError(f'Invalid type: {self.node_type} for ExpressionStatement')
        if not is_expression(self.expr):
            raise TypeError(f'Invalid type: {self.expr.node_type} for expr stmt')

    def to_string(self) -> str:
        return f'{self.expr.to_string()};'
