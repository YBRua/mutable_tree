from ..node import NodeType
from .expression import Expression
from ..utils import is_primary_expression, is_expression
from typing import List
from . import PrimaryExpression


class CallExpression(Expression):

    def __init__(self, node_type: NodeType, callee: PrimaryExpression,
                 args: List[Expression]):
        super().__init__(node_type)
        self.callee = callee
        self.args = args

    def _check_types(self):
        if self.node_type != NodeType.CALL_EXPR:
            raise TypeError(f'Invalid type: {self.node_type} for CallExpression')
        if not is_primary_expression(self.callee):
            raise TypeError(f'Invalid type: {self.callee.node_type} for callee')
        for i, arg in enumerate(self.args):
            if not is_expression(arg):
                raise TypeError(f'Invalid type: {arg.node_type} for call argument {i}')

    def to_string(self) -> str:
        arg_list = ", ".join(arg.to_string() for arg in self.args)
        return f'{self.callee.to_string()}({arg_list})'
