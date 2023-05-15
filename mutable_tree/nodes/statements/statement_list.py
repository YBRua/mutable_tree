from ..node import Node, NodeType
from .statement import Statement
from .statement import is_statement
from ..utils import throw_invalid_type
from typing import List


class StatementList(Statement):

    def __init__(self, node_type: NodeType, exprs: List[Statement]):
        super().__init__(node_type)
        self.stmts = exprs
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.STATEMENT_LIST:
            throw_invalid_type(self.node_type, self)

        for i, stmt in enumerate(self.stmts):
            if not is_statement(stmt):
                throw_invalid_type(stmt.node_type, self, f'stmt#{i}')

    def get_children(self) -> List[Node]:
        return self.stmts

    def get_children_names(self) -> List[str]:
        return ['stmts']
