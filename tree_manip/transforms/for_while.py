from mutable_tree.nodes import Node, NodeType
from mutable_tree.nodes import node_factory
from mutable_tree.nodes import ForStatement, WhileStatement, BlockStatement
from mutable_tree.nodes import is_expression
from typing import List


def _collect_for_nodes(root: Node) -> List[ForStatement]:
    for_nodes = []

    def _collect_for_nodes_impl(node: Node):
        if node.node_type == NodeType.FOR_STMT:
            for_nodes.append(node)
        for child in node.get_children():
            _collect_for_nodes_impl(child)

    _collect_for_nodes_impl(root)
    return for_nodes


def for_stmt_to_while_stmt(for_stmt: ForStatement) -> WhileStatement:
    cond = for_stmt.condition

    if cond is None:
        cond = node_factory.create_literal('true')
    update = for_stmt.update
    if update is None:
        update = []

    for_body = for_stmt.body
    if for_body.node_type != NodeType.BLOCK_STMT:
        body_stmts = [for_body]
    else:
        assert isinstance(for_body, BlockStatement)
        body_stmts = for_body.stmts

    for u in update.get_children():
        assert is_expression(u)
        body_stmts.append(node_factory.create_expression_stmt(u))
    while_body = node_factory.create_block_stmt(body_stmts)

    return node_factory.create_while_stmt(cond, while_body)


def for_to_while(root: Node) -> Node:
    for_nodes = _collect_for_nodes(root)
    for node in for_nodes:
        node = for_stmt_to_while_stmt(node)
    return root
