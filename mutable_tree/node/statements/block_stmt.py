from ..node import NodeType
from .statement import Statement
from .statement import is_statement
from typing import List


class BlockStatement(Statement):

    def __init__(self, node_type: NodeType, stmts: List[Statement]):
        super().__init__(node_type)
        self.stmts = stmts
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.BLOCK_STMT:
            raise TypeError(f'Invalid type: {self.node_type} for BlockStatement')
        for i, stmt in enumerate(self.stmts):
            if not is_statement(stmt):
                raise TypeError(f'Invalid type: {stmt.node_type} for block stmt {i}')

    def to_string(self) -> str:
        return '{\n' + '\n'.join(stmt.to_string() for stmt in self.stmts) + '\n}'
