from ..node import Node, NodeType
from .statement import Statement
from .statement import is_statement
from ..expressions import Expression
from ..expressions import is_expression
from ..utils import throw_invalid_type
from typing import List, Optional


class SwitchCase(Node):

    def __init__(self,
                 node_type: NodeType,
                 stmts: List[Statement],
                 case: Optional[Expression] = None):
        super().__init__(node_type)
        self.case = case
        self.stmts = stmts
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.SWITCH_CASE:
            throw_invalid_type(self.node_type, self)
        if self.case is not None and not is_expression(self.case):
            throw_invalid_type(self.case.node_type, self, attr='case')
        for i, stmt in enumerate(self.stmts):
            if not is_statement(stmt):
                throw_invalid_type(stmt.node_type, self, attr=f'stmts#{i}')

    def to_string(self) -> str:
        if self.case is not None:
            case_str = f'case {self.case.to_string()}:'
        else:
            case_str = 'default:'
        stmts_str = '\n'.join([stmt.to_string() for stmt in self.stmts])
        return f'{case_str}\n{stmts_str}'

    def get_children(self) -> List[Node]:
        if self.case is not None:
            return [self.case] + self.stmts
        else:
            return self.stmts


class SwitchStatement(Statement):

    def __init__(self, node_type: NodeType, condition: Expression,
                 body: List[SwitchCase]):
        super().__init__(node_type)
        self.condition = condition
        self.body = body
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.SWITCH_STMT:
            throw_invalid_type(self.node_type, self)
        for i, case in enumerate(self.body):
            if case.node_type != NodeType.SWITCH_CASE:
                throw_invalid_type(case.node_type, self, attr=f'case#{i}')

    def to_string(self) -> str:
        cond_str = self.condition.to_string()
        body_str = '\n'.join([case.to_string() for case in self.body])
        return f'switch ({cond_str}) {{\n{body_str}\n}}'

    def get_children(self) -> List[Node]:
        return [self.condition] + self.body
