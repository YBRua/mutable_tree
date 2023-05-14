from enum import Enum
from ..node import NodeType
from .expression import Expression
from ..utils import is_expression


class UpdateOps(Enum):
    INCREMENT = '++'
    DECREMENT = '--'


class UpdateExpression(Expression):

    def __init__(self, node_type: NodeType, operand: Expression, op: UpdateOps):
        super().__init__(node_type)
        self.operand = operand
        self.op = op
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.UPDATE_EXPR:
            raise TypeError(f'Invalid type: {self.node_type} for UpdateExpression')
        if not is_expression(self.operand):
            raise TypeError(f'Invalid type: {self.operand.node_type} for update operand')

    def to_string(self) -> str:
        return f'{str(self.op)} {self.operand.to_string()}'
