from ..node import NodeType
from .expression import Expression
from ..utils import is_expression


class TernaryExpression(Expression):

    def __init__(self, node_type: NodeType, condition: Expression,
                 consequence: Expression, alternative: Expression):
        super().__init__(node_type)
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def _check_types(self):
        if self.node_type != NodeType.TERNARY_EXPR:
            raise TypeError(f'Invalid type: {self.node_type} for TernaryExpression.')
        if not is_expression(self.condition):
            raise TypeError(
                f'Invalid type: {self.condition.node_type} for ternary condition.')
        if not is_expression(self.consequence):
            raise TypeError(
                f'Invalid type: {self.consequence.node_type} for ternary consequence.')
        if not is_expression(self.alternative):
            raise TypeError(
                f'Invalid type: {self.alternative.node_type} for ternary alternative.')

    def to_string(self) -> str:
        return (f'{self.condition.to_string()} ? '
                f'{self.consequence.to_string()} : '
                f'{self.alternative.to_string()}')
