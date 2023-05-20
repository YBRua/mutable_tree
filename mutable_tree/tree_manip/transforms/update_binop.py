from ..visitor import TransformingVisitor
from mutable_tree.nodes import Node
from mutable_tree.nodes import Literal, BinaryExpression
from mutable_tree.nodes import AssignmentOps, BinaryOps, UpdateOps
from mutable_tree.nodes import node_factory
from mutable_tree.nodes import UpdateExpression, AssignmentExpression
from typing import Optional


class BinopUpdateVisitor(TransformingVisitor):

    assign_op_to_bin_op = {
        AssignmentOps.PLUS_EQUAL: BinaryOps.PLUS,
        AssignmentOps.MINUS_EQUAL: BinaryOps.MINUS
    }
    update_op_to_bin_op = {
        UpdateOps.INCREMENT: BinaryOps.PLUS,
        UpdateOps.DECREMENT: BinaryOps.MINUS
    }

    def _create_new_node(self, expr: Node, op: BinaryOps):
        literal = node_factory.create_literal('1')
        binop_expr = node_factory.create_binary_expr(expr, literal, op)
        return node_factory.create_assignment_expr(expr, binop_expr, AssignmentOps.EQUAL)

    def visit_UpdateExpression(self,
                               expr: UpdateExpression,
                               parent: Optional[Node] = None,
                               parent_attr: Optional[str] = None):
        self.generic_visit(expr, parent, parent_attr)
        new_node = self._create_new_node(expr.operand, self.update_op_to_bin_op[expr.op])
        return (True, [new_node])

    def visit_AssignmentExpression(self,
                                   expr: AssignmentExpression,
                                   parent: Optional[Node] = None,
                                   parent_attr: Optional[str] = None):
        self.generic_visit(expr, parent, parent_attr)

        if (expr.op == AssignmentOps.PLUS_EQUAL or expr.op == AssignmentOps.MINUS_EQUAL):
            # i += 1
            rhs = expr.right
            # FIXME: (ybrua) values for literals are currently always strings
            if isinstance(rhs, Literal) and rhs.value == '1':
                new_node = self._create_new_node(expr.left,
                                                 self.assign_op_to_bin_op[expr.op])
                return (True, [new_node])

        return (False, None)
