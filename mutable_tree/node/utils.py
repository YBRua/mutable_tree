from .node import Node, NodeType
from .expressions import Expression


def is_expression(node: Node):
    return isinstance(node, Expression)


def is_primary_expression(node: Node):
    nt = node.node_type
    return nt in {
        NodeType.LITERAL, NodeType.IDENTIFIER, NodeType.THIS_EXPR,
        NodeType.PARENTHESIZED_EXPR, NodeType.NEW_EXPR, NodeType.CALL_EXPR,
        NodeType.FIELD_ACCESS, NodeType.ARRAY_ACCESS
    }
