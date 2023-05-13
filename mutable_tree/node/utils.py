from .node import Node
from .expressions import Expression


def is_expression(node: Node):
    return isinstance(node, Expression)
