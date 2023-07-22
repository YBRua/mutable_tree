# https://github.com/tree-sitter/tree-sitter-javascript/blob/master/grammar.js
import tree_sitter
from ...nodes import Expression, Statement
from ...nodes import (ArrayAccess, ArrayCreationExpression, ArrayExpression,
                      AssignmentExpression, BinaryExpression, CallExpression,
                      CastExpression, FieldAccess, Identifier, InstanceofExpression,
                      Literal, NewExpression, TernaryExpression, ThisExpression,
                      UnaryExpression, UpdateExpression, ParenthesizedExpression,
                      ExpressionList, LambdaExpression, SpreadElement, AwaitExpression)
from ...nodes import (AssertStatement, BlockStatement, BreakStatement, ContinueStatement,
                      DoStatement, EmptyStatement, ExpressionStatement, ForInStatement,
                      ForStatement, IfStatement, LabeledStatement, ReturnStatement,
                      SwitchStatement, SwitchCase, SwitchCaseList, ThrowStatement,
                      TryStatement, CatchClause, FinallyClause, TryHandlers,
                      WhileStatement, YieldStatement, TryResource, TryResourceList,
                      TryWithResourcesStatement, SynchronizedStatement)
from ...nodes import (Declarator, VariableDeclarator, ArrayDeclarator,
                      InitializingDeclarator, DeclaratorType, LocalVariableDeclaration)
from ...nodes import (FormalParameter, InferredParameter, TypedFormalParameter,
                      SpreadParameter, FormalParameterList, FunctionHeader,
                      FunctionDeclaration)
from ...nodes import (Modifier, ModifierList)
from ...nodes import Program
from ...nodes import TypeIdentifier, Dimensions, TypeParameter, TypeParameterList
from ...nodes import get_assignment_op, get_binary_op, get_unary_op, get_update_op
from ...nodes import node_factory
from typing import Tuple, Optional, List


def convert_program(node: tree_sitter.Node) -> Program:
    assert node.type == 'program'
    stmts = []
    for ch in node.children:
        stmts.append(convert_statement(ch))

    return node_factory.create_program(node_factory.create_statement_list(stmts))


def convert_statement(node: tree_sitter.Node) -> Statement:
    stmt_convertors = {
        'expression_statement': convert_expression_stmt,
        'statement_block': convert_block_stmt,
    }
    return stmt_convertors[node.type](node)


def convert_expression(node: tree_sitter.Node) -> Expression:
    expr_convertors = {
        'identifier': convert_identifier,
        'property_identifier': convert_identifier,
        'number': convert_literal,
        'string': convert_literal,
        'template_string': convert_literal,
        'regex': convert_literal,
        'true': convert_literal,
        'false': convert_literal,
        'null': convert_literal,
        'undefined': convert_literal,
        'subscript_expression': convert_subscript_expression,
        'member_expression': convert_member_expression,
        'parenthesized_expression': convert_parenthesized_expression,
        'spread_element': convert_spread_element,
        'array': convert_array,
        'call_expression': convert_call_expression,
        'assignment_expression': convert_assignment_expr,
        'augmented_assignment_expression': convert_augmented_assignment_expr,
        'await_expression': convert_await_expr,
        'unary_expression': convert_unary_expr,
        'binary_expression': convert_binary_expr,
        'ternary_expression': convert_ternary_expr,
        'update_expression': convert_update_expr,
        'new_expression': convert_new_expr,
        'yield_expression': convert_yield_expr,
        'this': convert_this_expr,
    }
    return expr_convertors[node.type](node)


def convert_simple_type(node: tree_sitter.Node) -> TypeIdentifier:
    return node_factory.create_type_identifier(node.text.decode())


def convert_identifier(node: tree_sitter.Node) -> Identifier:
    name = node.text.decode()
    return node_factory.create_identifier(name)


def convert_literal(node: tree_sitter.Node) -> Literal:
    value = node.text.decode()
    return node_factory.create_literal(value)


def convert_subscript_expression(node: tree_sitter.Node) -> ArrayAccess:
    object_expr = convert_expression(node.child_by_field_name('object'))
    optional = node.child_by_field_name('optional_chain') is not None
    index_expr = convert_expression(node.child_by_field_name('index'))

    return node_factory.create_array_access(object_expr, index_expr, optional)


def convert_member_expression(node: tree_sitter.Node) -> FieldAccess:
    object_expr = convert_expression(node.child_by_field_name('object'))
    optional = node.child_by_field_name('optional_chain') is not None
    member_name = convert_expression(node.child_by_field_name('property'))
    return node_factory.create_field_access(object_expr, member_name, optional=optional)


def convert_parenthesized_expression(node: tree_sitter.Node) -> ParenthesizedExpression:
    if node.child_count != 3:
        raise AssertionError('parenthesized_expression should have 3 children')

    expr = convert_expression(node.children[1])
    return node_factory.create_parenthesized_expr(expr)


def convert_spread_element(node: tree_sitter.Node) -> SpreadElement:
    if node.child_count != 2:
        raise AssertionError('spread_element should have 2 children')

    expr = convert_expression(node.children[1])
    return node_factory.create_spread_element(expr)


def convert_array(node: tree_sitter.Node) -> ArrayExpression:
    elements = []
    for ch in node.children[1:-1]:
        if ch.type == ',':
            continue
        elements.append(convert_expression(ch))
    return node_factory.create_array_expr(node_factory.create_expression_list(elements))


def convert_argument_list(node: tree_sitter.Node) -> ExpressionList:
    args = []
    for ch in node.children[1:-1]:
        # skip parenthesis and comma sep
        if ch.type == ',':
            continue
        args.append(convert_expression(ch))
    return node_factory.create_expression_list(args)


def convert_call_expression(node: tree_sitter.Node) -> CallExpression:
    callee_node = node.child_by_field_name('function')
    arg_node = node.child_by_field_name('arguments')
    optional = node.child_by_field_name('optional_chain') is not None

    callee_expr = convert_expression(callee_node)
    args = convert_argument_list(arg_node)

    return node_factory.create_call_expr(callee_expr, args, optional)


def convert_assignment_expr(node: tree_sitter.Node) -> AssignmentExpression:
    if node.child_count != 3:
        raise AssertionError('assignment_expression should have 3 children')

    lhs = convert_expression(node.child_by_field_name('left'))
    rhs = convert_expression(node.child_by_field_name('right'))
    op = get_assignment_op(node.children[1].text.decode())
    return node_factory.create_assignment_expr(lhs, rhs, op)


def convert_augmented_assignment_expr(node: tree_sitter.Node) -> AssignmentExpression:
    lhs = convert_expression(node.child_by_field_name('left'))
    rhs = convert_expression(node.child_by_field_name('right'))
    op = get_assignment_op(node.child_by_field_name('operator').text.decode())
    return node_factory.create_assignment_expr(lhs, rhs, op)


def convert_await_expr(node: tree_sitter.Node) -> AwaitExpression:
    if node.child_count != 2:
        raise AssertionError('await_expression should have 2 children')

    expr = convert_expression(node.children[1])
    return node_factory.create_await_expr(expr)


def convert_unary_expr(node: tree_sitter.Node) -> UnaryExpression:
    op = get_unary_op(node.child_by_field_name('operator').text.decode())
    operand = convert_expression(node.child_by_field_name('argument'))

    if op == 'delete':
        return node_factory.create_delete_expr(operand)
    else:
        return node_factory.create_unary_expr(operand, op)


def convert_binary_expr(node: tree_sitter.Node) -> BinaryExpression:
    lhs = convert_expression(node.child_by_field_name('left'))
    rhs = convert_expression(node.child_by_field_name('right'))
    op = get_binary_op(node.child_by_field_name('operator').text.decode())

    return node_factory.create_binary_expr(lhs, rhs, op)


def convert_ternary_expr(node: tree_sitter.Node) -> TernaryExpression:
    condition_node = node.child_by_field_name('condition')
    consequence_node = node.child_by_field_name('consequence')
    alternate_node = node.child_by_field_name('alternative')

    condition = convert_expression(condition_node)
    consequence = convert_expression(consequence_node)
    alternate = convert_expression(alternate_node)
    return node_factory.create_ternary_expr(condition, consequence, alternate)


def convert_update_expr(node: tree_sitter.Node) -> UpdateExpression:
    if node.children[0].type not in {'++', '--'}:
        prefix = False
        op = get_update_op(node.children[1].text.decode())
        expr = convert_expression(node.children[0])
    else:
        prefix = True
        op = get_update_op(node.children[0].text.decode())
        expr = convert_expression(node.children[1])
    return node_factory.create_update_expr(expr, op, prefix)


def convert_new_expr(node: tree_sitter.Node) -> NewExpression:
    # TODO: type_argument, constructor
    # type_arg_node = node.child_by_field_name('type_arguments')
    type_node = node.child_by_field_name('constructor')
    args_node = node.child_by_field_name('arguments')

    # FIXME: constructor should be primary expression
    type_id = convert_simple_type(type_node)
    args = convert_argument_list(args_node)

    return node_factory.create_new_expr(type_id, args)


def convert_yield_expr(node: tree_sitter.Node) -> YieldStatement:
    if node.child_count == 1:
        return node_factory.create_yield_stmt()
    elif node.child_count == 2:
        expr = convert_expression(node.children[1])
        return node_factory.create_yield_stmt(expr)
    elif node.child_count == 3:
        expr = convert_expression(node.children[2])
        return node_factory.create_yield_stmt(expr, is_delegate=True)
    else:
        raise AssertionError(f'yield_expression has {node.child_count} children')


def convert_this_expr(node: tree_sitter.Node) -> ThisExpression:
    return node_factory.create_this_expr()


def convert_expression_stmt(node: tree_sitter.Node) -> ExpressionStatement:
    expr = convert_expression(node.children[0])
    return node_factory.create_expression_stmt(expr)


def convert_block_stmt(node: tree_sitter.Node) -> BlockStatement:
    stmts = []
    for stmt_node in node.children:
        if stmt_node.type in {'{', '}', ';'}:
            continue
        stmts.append(convert_statement(stmt_node))
    stmts = node_factory.create_statement_list(stmts)
    return node_factory.create_block_stmt(stmts)
