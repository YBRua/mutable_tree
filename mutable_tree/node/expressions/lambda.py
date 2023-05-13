from ..node import Node, NodeType
from .expression import Expression
from typing import List


class LambdaExpression(Expression):

    def __init__(self, node_type: NodeType, params: List[Node], body: Expression):
        super().__init__(node_type)
        # TODO
