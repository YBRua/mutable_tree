from ..node import NodeType
from .statement import Statement
from ..expressions import Expression
from ..utils import is_expression
from ..utils import throw_invalid_type


class ThrowStatement(Statement):

    def __init__(self, node_type: NodeType, expr: Expression):
        super().__init__(node_type)
        self.expr = expr
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.THROW_STMT:
            throw_invalid_type(self.node_type, self)
        if not is_expression(self.expr):
            throw_invalid_type(self.expr.node_type, self, attr='expr')

    def to_string(self) -> str:
        return f'throw {self.expr.to_string()};'
