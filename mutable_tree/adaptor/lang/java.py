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
        'binary_expression': convert_binary_expr,
        'method_invocation': convert_call_expr,
        'field_access': convert_field_access,
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


def convert_binary_expr(node: tree_sitter.Node) -> BinaryExpression:
    lhs = convert_expression(node.child_by_field_name('left'))
    rhs = convert_expression(node.child_by_field_name('right'))
    op = get_binary_op(node.child_by_field_name('operator').text.decode())
    return node_factory.create_binary_expr(lhs, rhs, op)


def convert_field_access(node: tree_sitter.Node) -> FieldAccess:
    if node.child_count != 3:
        raise RuntimeError(f'field access with {node.child_count} children')

    obj_expr = convert_expression(node.child_by_field_name('object'))
    name_expr = convert_expression(node.child_by_field_name('field'))
    return node_factory.create_field_access(obj_expr, name_expr)


def convert_call_expr(node: tree_sitter.Node) -> CallExpression:
    if node.child_count != 2 and node.child_count != 4:
        raise RuntimeError(f'call expr with {node.child_count} children')

    arg_node = node.child_by_field_name('arguments')
    args = []
    for arg in arg_node.children[1:-1]:
        # skip parenthesis and comma sep
        if arg.text.decode() == ',':
            continue
        args.append(convert_expression(arg))

    name_expr = convert_expression(node.child_by_field_name('name'))
    obj_node = node.child_by_field_name('object')
    if obj_node is not None:
        obj_expr = convert_expression(obj_node)
        callee_expr = node_factory.create_field_access(obj_expr, name_expr)
    else:
        callee_expr = name_expr

    return node_factory.create_call_expr(callee_expr, args)


def convert_expression_stmt(node: tree_sitter.Node) -> ExpressionStatement:
    expr = convert_expression(node.children[0])
    return node_factory.create_expression_stmt(expr)
