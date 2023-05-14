import tree_sitter
from ...node import Node, Expression, Statement
from ...node import (ArrayAccess, ArrayExpression, AssignmentExpression, BinaryExpression,
                     CallExpression, CastExpression, FieldAccess, Identifier,
                     InstanceofExpression, Literal, NewExpression, TernaryExpression,
                     ThisExpression, UnaryExpression, UpdateExpression, PrimaryExpression)
from ...node import (AssertStatement, BlockStatement, BreakStatement, ContinueStatement,
                     DoStatement, ExpressionStatement, ForInStatement, ForStatement,
                     IfStatement, LabeledStatement, LocalVariableDeclaration,
                     ReturnStatement, SwitchStatement, ThrowStatement, TryStatement,
                     WhileStatement, YieldStatement)
from ...node import get_assignment_op, get_binary_op, get_unary_op, get_update_op
from ...node import node_factory


def convert_expression(node: tree_sitter.Node) -> Expression:
    expr_convertors = {
        'identifier': convert_identifier,
        'decimal_integer_literal': convert_literal,
        'hex_integer_literal': convert_literal,
        'octal_integer_literal': convert_literal,
        'binary_integer_literal': convert_literal,
        'decimal_floating_point_literal': convert_literal,
        'hex_floating_point_literal': convert_literal,
        'true': convert_literal,
        'false': convert_literal,
        'character_literal': convert_literal,
        'string_literal': convert_literal,
        'null_literal': convert_literal,
        'array_access': convert_array_access,
        'assignment_expression': convert_assignment_expr,
    }

    return expr_convertors[node.type](node)


def convert_statement(node: tree_sitter.Node) -> Statement:
    stmt_convertors = {
        'expression_statement': convert_expression_stmt,
    }

    return stmt_convertors[node.type](node)


def convert_identifier(node: tree_sitter.Node) -> Identifier:
    name = node.text.decode()
    return node_factory.create_identifier(name)


def convert_literal(node: tree_sitter.Node) -> Literal:
    value = node.text.decode()
    return node_factory.create_literal(value)


def convert_array_access(node: tree_sitter.Node) -> ArrayAccess:
    array_expr = convert_expression(node.child_by_field_name('array'))
    index_expr = convert_expression(node.child_by_field_name('index'))
    return node_factory.create_array_access(array_expr, index_expr)


def convert_array_expr(node: tree_sitter.Node) -> ArrayExpression:
    raise NotImplementedError('pending on variable initializer')


def convert_assignment_expr(node: tree_sitter.Node) -> AssignmentExpression:
    lhs = convert_expression(node.child_by_field_name('left'))
    rhs = convert_expression(node.child_by_field_name('right'))
    op = get_assignment_op(node.child_by_field_name('operator').text.decode())
    return node_factory.create_assignment_expr(lhs, rhs, op)


def convert_expression_stmt(node: tree_sitter.Node) -> ExpressionStatement:
    expr = convert_expression(node.children[0])
    return node_factory.create_expression_stmt(expr)
