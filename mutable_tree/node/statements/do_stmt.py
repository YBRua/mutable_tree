from ..node import NodeType
from .statement import Statement
from ..expressions import Expression
from ..utils import is_statement, is_expression


class DoStatement(Statement):

    def __init__(self, node_type: NodeType, body: Statement, condition: Expression):
        super().__init__(node_type)
        self.condition = condition
        self.body = body
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.DO_STMT:
            raise TypeError(f'Invalid type: {self.node_type} for DoStatement')
        if not is_statement(self.body):
            raise TypeError(f'Invalid type {self.body.node_type} for do body')
        if not is_expression(self.condition):
            raise TypeError(f'Invalid type {self.condition.node_type} for do condition')

    def to_string(self) -> str:
        return f'do\n {self.body.to_string()} \nwhile {self.condition.to_string()};'
