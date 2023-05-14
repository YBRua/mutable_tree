from .node import NodeType
from .expressions import Expression
from .expressions import BinaryOps, UnaryOps, UpdateOps, AssignmentOps
from .expressions import (ArrayAccess, ArrayExpression, AssignmentExpression,
                          BinaryExpression, CallExpression, CastExpression, FieldAccess,
                          Identifier, InstanceofExpression, Literal, NewExpression,
                          TernaryExpression, ThisExpression, UnaryExpression,
                          UpdateExpression, PrimaryExpression)
from .types import TypeIdentifier

from typing import Union, List


def create_identifier(name: str) -> Identifier:
    return Identifier(NodeType.IDENTIFIER, name)


def create_literal(value: str) -> Literal:
    return Literal(NodeType.LITERAL, value)


def create_assignment_expr(left: Union[Identifier, ArrayAccess, FieldAccess],
                           right: Expression, op: AssignmentOps) -> AssignmentExpression:
    return AssignmentExpression(NodeType.ASSIGNMENT_EXPR, left, right, op)


def create_binary_expr(left: Expression, right: Expression,
                       op: BinaryOps) -> BinaryExpression:
    return BinaryExpression(NodeType.BINARY_EXPR, left, right, op)


def create_unary_expr(expr: Expression, op: UnaryOps) -> UnaryExpression:
    return UnaryExpression(NodeType.UNARY_EXPR, expr, op)


def create_update_expr(expr: Union[Identifier, FieldAccess], op: UpdateOps,
                       prefix: bool) -> UpdateExpression:
    return UpdateExpression(NodeType.UPDATE_EXPR, expr, op, prefix)


def create_array_access(array: PrimaryExpression, index: Expression) -> ArrayAccess:
    return ArrayAccess(NodeType.ARRAY_ACCESS, array, index)


def create_array_expr(elements: List[Expression]) -> ArrayExpression:
    return ArrayExpression(NodeType.ARRAY_EXPR, elements)


def create_call_expr(callee: PrimaryExpression, args: List[Expression]) -> CallExpression:
    return CallExpression(NodeType.CALL_EXPR, callee, args)


def create_cast_expr(type_name: TypeIdentifier, expr: Expression) -> CastExpression:
    return CastExpression(NodeType.CAST_EXPR, type_name, expr)


def create_field_access(obj: PrimaryExpression, field: Identifier) -> FieldAccess:
    return FieldAccess(NodeType.FIELD_ACCESS, obj, field)


def create_instanceof_expr(expr: Expression,
                           type_name: TypeIdentifier) -> InstanceofExpression:
    return InstanceofExpression(NodeType.INSTANCEOF_EXPR, expr, type_name)


def create_new_expr(type_name: TypeIdentifier, args: List[Expression]) -> NewExpression:
    return NewExpression(NodeType.NEW_EXPR, type_name, args)


def create_ternary_expr(condition: Expression, consequence: Expression,
                        alternate: Expression) -> TernaryExpression:
    return TernaryExpression(NodeType.TERNARY_EXPR, condition, consequence, alternate)


def create_this_expr() -> ThisExpression:
    return ThisExpression(NodeType.THIS_EXPR)
