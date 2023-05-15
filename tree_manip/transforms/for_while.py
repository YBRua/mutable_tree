from ..visitor import Visitor
from mutable_tree.nodes import Node, NodeType
from mutable_tree.nodes import node_factory
from mutable_tree.nodes import ForStatement
from mutable_tree.nodes import is_expression
from typing import Optional


class ForToWhileVisitor(Visitor):

    def visit_ForStatement(self,
                           node: ForStatement,
                           parent: Optional[Node] = None,
                           parent_attr: Optional[str] = None):
        init = node.init
        condition = node.condition
        update = node.update
        body = node.body

        if condition is None:
            condition = node_factory.create_literal('true')
        update_exprs = [] if update is None else update.get_children()

        if body.node_type != NodeType.BLOCK_STMT:
            body_stmts = [body]
        else:
            # get statement list from block statement
            body_stmts = body.get_children()[0].get_children()

        for u in update_exprs:
            assert is_expression(u)
            body_stmts.append(node_factory.create_expression_stmt(u))
        while_body = node_factory.create_block_stmt(
            node_factory.create_statement_list(body_stmts))

        while_stmt = node_factory.create_while_stmt(condition, while_body)
        parent.set_child_at(parent_attr, while_stmt)
