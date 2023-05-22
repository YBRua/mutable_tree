from .visitor import TransformingVisitor
from mutable_tree.nodes import Node
from mutable_tree.nodes import Literal, BinaryExpression
from mutable_tree.nodes import AssignmentOps, BinaryOps, UpdateOps
from mutable_tree.nodes import node_factory
from mutable_tree.nodes import UpdateExpression, AssignmentExpression
from typing import Optional


class AssignUpdateVisitor(TransformingVisitor):

    update_op_to_assign_op = {
        UpdateOps.INCREMENT: AssignmentOps.PLUS_EQUAL,
        UpdateOps.DECREMENT: AssignmentOps.MINUS_EQUAL
    }
    bin_op_to_assign_op = {
        BinaryOps.PLUS: AssignmentOps.PLUS_EQUAL,
        BinaryOps.MINUS: AssignmentOps.MINUS_EQUAL
    }

    def _create_new_node(self, expr: Node, op: AssignmentOps):
        literal = node_factory.create_literal('1')
        return node_factory.create_assignment_expr(expr, literal, op)

    def visit_UpdateExpression(self,
                               expr: UpdateExpression,
                               parent: Optional[Node] = None,
                               parent_attr: Optional[str] = None):
        self.generic_visit(expr, parent, parent_attr)
        new_node = self._create_new_node(expr.operand,
                                         self.update_op_to_assign_op[expr.op])
        return (True, [new_node])

    def visit_AssignmentExpression(self,
                                   expr: AssignmentExpression,
                                   parent: Optional[Node] = None,
                                   parent_attr: Optional[str] = None):
        self.generic_visit(expr, parent, parent_attr)

        if expr.op == AssignmentOps.EQUAL and isinstance(expr.right, BinaryExpression):
            # i = i + 1
            # NOTE: this visitor do not convert i = 1 + i
            bin_expr = expr.right
            binop = bin_expr.op
            if binop not in {BinaryOps.PLUS, BinaryOps.MINUS}:
                return (False, None)

            bin_lhs = bin_expr.left
            bin_rhs = bin_expr.right

            lhs_str = expr.left.to_string()
            bin_lhs_str = bin_lhs.to_string()
            if ((lhs_str == bin_lhs_str)
                    and (isinstance(bin_rhs, Literal) and bin_rhs.value == '1')):
                assign_op = self.bin_op_to_assign_op[binop]
                new_node = self._create_new_node(expr.left, assign_op)
                return (True, [new_node])

        return (False, None)