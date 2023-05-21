# https://github.com/tree-sitter/tree-sitter-c/blob/master/grammar.js
# https://github.com/tree-sitter/tree-sitter-cpp/blob/master/grammar.js
import tree_sitter
from ...nodes import Expression, Statement
from ...nodes import (ArrayAccess, ArrayCreationExpression, ArrayExpression,
                      AssignmentExpression, BinaryExpression, CallExpression,
                      CastExpression, FieldAccess, Identifier, InstanceofExpression,
                      Literal, NewExpression, TernaryExpression, ThisExpression,
                      UnaryExpression, UpdateExpression, ParenthesizedExpression,
                      ExpressionList, LambdaExpression, CommaExpression, SizeofExpression,
                      PointerExpression, DeleteExpression)
from ...nodes import (AssertStatement, BlockStatement, BreakStatement, ContinueStatement,
                      DoStatement, EmptyStatement, ExpressionStatement, ForInStatement,
                      ForStatement, IfStatement, LabeledStatement,
                      LocalVariableDeclaration, VariableDeclarator, ReturnStatement,
                      SwitchStatement, SwitchCase, SwitchCaseList, ThrowStatement,
                      TryStatement, CatchClause, FinallyClause, TryHandlers,
                      WhileStatement, YieldStatement, TryResource, TryResourceList,
                      TryWithResourcesStatement, SynchronizedStatement)
from ...nodes import (FormalParameter, SpreadParameter, FormalParameterList,
                      FunctionDeclarator, FunctionDeclaration)
from ...nodes import (Modifier, ModifierList)
from ...nodes import Program
from ...nodes import (TypeIdentifier, Dimensions, DimensionSpecifier, TypeParameter,
                      TypeParameterList)
from ...nodes import (get_assignment_op, get_binary_op, get_unary_op, get_update_op,
                      get_field_access_op, get_pointer_op)
from ...nodes import node_factory
from typing import Tuple, Optional, List


def convert_program(node: tree_sitter.Node) -> Program:
    assert node.type == 'translation_unit', node.type
    stmts = []
    for child in node.children:
        stmts.append(convert_statement(child))
    return node_factory.create_program(node_factory.create_statement_list(stmts))


def convert_expression(node: tree_sitter.Node) -> Expression:
    expr_convertors = {
        'identifier': convert_identifier,
        'field_identifier': convert_identifier,
        'number_literal': convert_literal,
        'string_literal': convert_literal,
        'true': convert_literal,
        'false': convert_literal,
        'null': convert_literal,
        'nullptr': convert_literal,
        'concatenated_string': convert_literal,
        'char_literal': convert_literal,
        'raw_string_literal': convert_literal,
        'user_defined_literal': convert_literal,
        'assignment_expression': convert_assignment_expr,
        'binary_expression': convert_binary_expr,
        'update_expression': convert_update_expr,
        'unary_expression': convert_unary_expr,
        'cast_expression': convert_cast_expr,
        'conditional_expression': convert_ternary_expr,
        'subscript_expression': convert_array_access,
        'call_expression': convert_call_expr,
        'field_expression': convert_field_access,
        'parenthesized_expression': convert_parenthesized_expr,
        'comma_expression': convert_comma_expr,
        'sizeof_expression': convert_sizeof_expr,
        'pointer_expression': convert_pointer_expr,
        'this': convert_this_expr,
        'new_expression': convert_new_expr,
        'delete_expression': convert_delete_expr,
    }

    return expr_convertors[node.type](node)


def convert_statement(node: tree_sitter.Node) -> Statement:
    stmt_convertors = {
        'expression_statement': convert_expression_stmt,
    }

    return stmt_convertors[node.type](node)


def convert_type(node: tree_sitter.Node) -> TypeIdentifier:
    type_convertors = {
        'type_descriptor': convert_simple_type,
        'primitive_type': convert_simple_type,
    }

    return type_convertors[node.type](node)


def convert_simple_type(node: tree_sitter.Node) -> TypeIdentifier:
    return node_factory.create_type_identifier(node.text.decode())


def convert_identifier(node: tree_sitter.Node) -> Identifier:
    name = node.text.decode()
    return node_factory.create_identifier(name)


def convert_literal(node: tree_sitter.Node) -> Literal:
    value = node.text.decode()
    return node_factory.create_literal(value)


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


def convert_unary_expr(node: tree_sitter.Node) -> UnaryExpression:
    op = get_unary_op(node.child_by_field_name('operator').text.decode())
    operand = convert_expression(node.child_by_field_name('argument'))
    return node_factory.create_unary_expr(operand, op)


def convert_cast_expr(node: tree_sitter.Node) -> CastExpression:
    # TODO: type intersections
    type_node = node.child_by_field_name('type')
    value_node = node.child_by_field_name('value')

    type_id = convert_type(type_node)
    value_expr = convert_expression(value_node)
    return node_factory.create_cast_expr(type_id, value_expr)


def convert_ternary_expr(node: tree_sitter.Node) -> TernaryExpression:
    condition_node = node.child_by_field_name('condition')
    consequence_node = node.child_by_field_name('consequence')
    alternate_node = node.child_by_field_name('alternative')

    condition = convert_expression(condition_node)
    consequence = convert_expression(consequence_node)
    alternate = convert_expression(alternate_node)
    return node_factory.create_ternary_expr(condition, consequence, alternate)


def convert_array_access(node: tree_sitter.Node) -> ArrayAccess:
    array_expr = convert_expression(node.child_by_field_name('argument'))
    index_expr = convert_expression(node.child_by_field_name('index'))
    return node_factory.create_array_access(array_expr, index_expr)


def convert_argument_list(node: tree_sitter.Node) -> ExpressionList:
    args = []
    for ch in node.children[1:-1]:
        # skip parenthesis and comma sep
        if ch.type == ',':
            continue
        args.append(convert_expression(ch))
    return node_factory.create_expression_list(args)


def convert_call_expr(node: tree_sitter.Node) -> CallExpression:
    arg_node = node.child_by_field_name('arguments')
    args = convert_argument_list(arg_node)
    callee_node = node.child_by_field_name('function')
    if callee_node.type == 'primitive_type':
        callee = convert_type(callee_node)
    else:
        callee = convert_expression(node.child_by_field_name('function'))
    return node_factory.create_call_expr(callee, args)


def convert_field_access(node: tree_sitter.Node) -> FieldAccess:
    if node.child_count != 3:
        raise RuntimeError(f'field access with {node.child_count} children')

    obj = convert_expression(node.child_by_field_name('argument'))
    name = convert_expression(node.child_by_field_name('field'))
    op = get_field_access_op(node.child_by_field_name('operator').text.decode())

    return node_factory.create_field_access(obj, name, op)


def convert_parenthesized_expr(node: tree_sitter.Node) -> ParenthesizedExpression:
    assert node.child_count == 3, 'parenthesized expr with != 3 children'
    expr = convert_expression(node.children[1])
    return node_factory.create_parenthesized_expr(expr)


def convert_comma_expr(node: tree_sitter.Node) -> CommaExpression:
    left = convert_expression(node.child_by_field_name('left'))
    right = convert_expression(node.child_by_field_name('right'))
    return node_factory.create_comma_expr(left, right)


def convert_sizeof_expr(node: tree_sitter.Node) -> SizeofExpression:
    value_node = node.child_by_field_name('value')
    if value_node is not None:
        value = convert_expression(value_node)
        return node_factory.create_sizeof_expr(value)

    # must be a type
    type_node = node.child_by_field_name('type')
    type_id = convert_type(type_node)
    return node_factory.create_sizeof_expr(type_id)


def convert_pointer_expr(node: tree_sitter.Node) -> PointerExpression:
    expr = convert_expression(node.child_by_field_name('argument'))
    op = get_pointer_op(node.child_by_field_name('operator').text.decode())
    return node_factory.create_pointer_expr(expr, op)


def convert_this_expr(node: tree_sitter.Node) -> ThisExpression:
    return node_factory.create_this_expr()


def convert_new_declarator(node: tree_sitter.Node) -> Dimensions:

    def _convert_child_declarator(node: tree_sitter.Node) -> List[DimensionSpecifier]:
        if node.child_count == 3:
            length = convert_expression(node.child_by_field_name('length'))
            return [node_factory.create_dimension_specifier(length)]
        elif node.child_count == 4:
            length = convert_expression(node.child_by_field_name('length'))
            return ([node_factory.create_dimension_specifier(length)] +
                    _convert_child_declarator(node.children[-1]))
        else:
            raise ValueError(f'invalid child count {node.child_count}')

    specifiers = _convert_child_declarator(node)
    return node_factory.create_dimensions(specifiers)


def convert_new_expr(node: tree_sitter.Node) -> NewExpression:
    placement_node = node.child_by_field_name('placement')
    if placement_node is not None:
        raise NotImplementedError('placement new')
    type_node = node.child_by_field_name('type')
    declarator_node = node.child_by_field_name('declarator')

    type_str = type_node.text.decode()
    if declarator_node is not None:
        new_declarator = convert_new_declarator(declarator_node)
    else:
        new_declarator = None

    type_id = node_factory.create_type_identifier(type_str, new_declarator)

    arguments_node = node.child_by_field_name('arguments')
    if arguments_node is not None:
        arguments = convert_argument_list(arguments_node)
    else:
        arguments = None

    return node_factory.create_new_expr(type_id, arguments)


def convert_delete_expr(node: tree_sitter.Node) -> DeleteExpression:
    expr = convert_expression(node.children[-1])
    is_array = node.children[-2].type == ']'
    return node_factory.create_delete_expr(expr, is_array)


def convert_expression_stmt(node: tree_sitter.Node) -> ExpressionStatement:
    expr = convert_expression(node.children[0])
    return node_factory.create_expression_stmt(expr)
