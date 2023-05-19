from ..node import Node, NodeType
from .statement import Statement
from .statement import is_statement
from ..expressions import ParenthesizedExpression
from ..utils import throw_invalid_type
from typing import List, Optional


class IfStatement(Statement):

    def __init__(self,
                 node_type: NodeType,
                 condition: ParenthesizedExpression,
                 consequence: Statement,
                 alternate: Optional[Statement] = None):
        super().__init__(node_type)
        self.condition = condition
        self.consequence = consequence
        self.alternate = alternate
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.IF_STMT:
            throw_invalid_type(self.node_type, self)
        if self.condition.node_type != NodeType.PARENTHESIZED_EXPR:
            throw_invalid_type(self.condition.node_type, self, attr='condition')
        if not is_statement(self.consequence):
            throw_invalid_type(self.consequence.node_type, self, attr='consequence')
        if self.alternate is not None and not is_statement(self.alternate):
            throw_invalid_type(self.alternate.node_type, self, attr='alternate')

    def to_string(self) -> str:
        cond_str = self.condition.to_string()
        then_str = self.consequence.to_string()
        if self.alternate is None:
            return f'if {cond_str} {then_str}'
        else:
            else_str = self.alternate.to_string()
            return f'if {cond_str} {then_str} else {else_str}'

    def get_children(self) -> List[Node]:
        if self.alternate is None:
            return [self.condition, self.consequence]
        else:
            return [self.condition, self.consequence, self.alternate]

    def get_children_names(self) -> List[str]:
        return ['condition', 'consequence', 'alternate']
