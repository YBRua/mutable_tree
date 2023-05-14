from ..node import NodeType
from ..types import TypeIdentifier
from .expression import Expression
from .expression import is_expression
from typing import List


class NewExpression(Expression):

    def __init__(self, node_type: NodeType, type: TypeIdentifier, args: List[Expression]):
        super().__init__(node_type)
        self.type = type
        self.args = args

    def _check_types(self):
        if self.node_type != NodeType.CALL_EXPR:
            raise TypeError(f'Invalid type: {self.node_type} for NewExpression')
        if self.type.node_type != NodeType.TYPE_IDENTIFIER:
            raise TypeError(f'Invalid type: {self.type.node_type} for type')
        for i, arg in enumerate(self.args):
            if not is_expression(arg):
                raise TypeError(f'Invalid type: {arg.node_type} for new argument {i}')

    def to_string(self) -> str:
        arg_list = ", ".join(arg.to_string() for arg in self.args)
        return f'new {self.type.to_string()}({arg_list})'
