from .node import Node, NodeType
from .expressions import Expression
from .statements import Statement
from typing import Optional


def is_expression(node: Node):
    return isinstance(node, Expression)


def is_primary_expression(node: Node):
    nt = node.node_type
    return nt in {
        NodeType.LITERAL, NodeType.IDENTIFIER, NodeType.THIS_EXPR,
        NodeType.PARENTHESIZED_EXPR, NodeType.NEW_EXPR, NodeType.CALL_EXPR,
        NodeType.FIELD_ACCESS, NodeType.ARRAY_ACCESS
    }


def is_statement(node: Node):
    return isinstance(node, Statement)


def throw_invalid_type(ty: NodeType, obj: Node, attr: Optional[str] = None):
    if attr is not None:
        msg = f'Invalid type: {ty} for {attr} of {type(obj).__name__}'
    else:
        msg = f'Invalid type: {ty} for {type(obj).__name__}'
    raise TypeError(msg)
