from ..node import Node, NodeType
from .expression import Expression
from .expression import is_expression
from ..utils import throw_invalid_type
from typing import List


class ExpressionList(Expression):

    def __init__(self, node_type: NodeType, exprs: List[Expression]):
        super().__init__(node_type)
        self.exprs = exprs
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.EXPRESSION_LIST:
            throw_invalid_type(self.node_type, self)

        for i, expr in enumerate(self.exprs):
            if not is_expression(expr):
                throw_invalid_type(expr.node_type, self, f'expr#{i}')

    def get_children(self) -> List[Node]:
        return self.exprs

    def get_children_names(self) -> List[str]:
        return list(map(str, range(len(self.exprs))))
