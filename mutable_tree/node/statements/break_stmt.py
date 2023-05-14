from ..node import NodeType
from .statement import Statement
from ..expressions import Expression
from typing import Optional


class BreakStatement(Statement):

    def __init__(self, node_type: NodeType, label: Optional[Expression] = None):
        super().__init__(node_type)
        self.label = label

    def _check_types(self):
        if self.node_type != NodeType.BREAK_STMT:
            raise TypeError(f'Invalid type: {self.node_type} for BreakStatement')
        if self.label.node_type != NodeType.IDENTIFIER:
            raise TypeError(f'Invalid type: {self.label.node_type} for break label')

    def to_string(self) -> str:
        if self.label is not None:
            return f'break {self.label.to_string()};'
        else:
            return 'break;'
