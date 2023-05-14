from ..node import NodeType
from .statement import Statement
from .statement import is_statement
from ..expressions import Expression
from ..expressions import is_expression
from ..utils import throw_invalid_type


class WhileStatement(Statement):

    def __init__(self, node_type: NodeType, condition: Expression, body: Statement):
        super().__init__(node_type)
        self.condition = condition
        self.body = body
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.WHILE_STMT:
            throw_invalid_type(self.node_type, self)
        if not is_expression(self.condition):
            throw_invalid_type(self.condition.node_type, self, attr='condition')
        if not is_statement(self.body):
            throw_invalid_type(self.body.node_type, self, attr='body')

    def to_string(self) -> str:
        cond_str = self.condition.to_string()
        body_str = self.body.to_string()

        return f'while ({cond_str}) {body_str}'
