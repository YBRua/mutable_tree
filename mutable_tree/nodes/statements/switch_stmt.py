from ..node import Node, NodeType
from .statement import Statement
from .statement_list import StatementList
from ..expressions import Expression
from ..expressions import is_expression
from ..utils import throw_invalid_type
from typing import List, Optional


class SwitchCase(Node):

    def __init__(self,
                 node_type: NodeType,
                 stmts: StatementList,
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
        if self.stmts.node_type != NodeType.STATEMENT_LIST:
            throw_invalid_type(self.stmts.node_type, self, attr='stmts')

    def to_string(self) -> str:
        if self.case is not None:
            case_str = f'case {self.case.to_string()}:'
        else:
            case_str = 'default:'
        stmts_str = '\n'.join([stmt.to_string() for stmt in self.stmts.get_children()])
        return f'{case_str}\n{stmts_str}'

    def get_children(self) -> List[Node]:
        if self.case is not None:
            return [self.case, self.stmts]
        else:
            return [self.stmts]


class SwitchCaseList(Node):

    def __init__(self, node_type: NodeType, cases: List[SwitchCase]):
        super().__init__(node_type)
        self.cases = cases
        self._check_types()

    def _check_types(self):
        for i, case in enumerate(self.cases):
            if case.node_type != NodeType.SWITCH_CASE:
                throw_invalid_type(case.node_type, self, attr=f'case#{i}')

    def get_children(self) -> List[Node]:
        return self.cases


class SwitchStatement(Statement):

    def __init__(self, node_type: NodeType, condition: Expression, cases: SwitchCaseList):
        super().__init__(node_type)
        self.condition = condition
        self.cases = cases
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.SWITCH_STMT:
            throw_invalid_type(self.node_type, self)
        if not is_expression(self.condition):
            throw_invalid_type(self.condition.node_type, self, attr='condition')
        if self.cases.node_type != NodeType.SWITCH_CASE_LIST:
            throw_invalid_type(self.cases.node_type, self, attr='cases')

    def to_string(self) -> str:
        cond_str = self.condition.to_string()
        body_str = '\n'.join([case.to_string() for case in self.cases.get_children()])
        return f'switch ({cond_str}) {{\n{body_str}\n}}'

    def get_children(self) -> List[Node]:
        return [self.condition, self.cases]
