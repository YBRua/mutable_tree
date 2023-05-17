import tree_sitter
from ...nodes import Node, Expression, Statement
from ...nodes import (ArrayAccess, ArrayExpression, AssignmentExpression,
                      BinaryExpression, CallExpression, CastExpression, FieldAccess,
                      Identifier, InstanceofExpression, Literal, NewExpression,
                      TernaryExpression, ThisExpression, UnaryExpression,
                      UpdateExpression, PrimaryExpression, ExpressionList)
from ...nodes import (AssertStatement, BlockStatement, BreakStatement, ContinueStatement,
                      DoStatement, EmptyStatement, ExpressionStatement, ForInStatement,
                      ForStatement, IfStatement, LabeledStatement,
                      LocalVariableDeclaration, VariableDeclarator, ReturnStatement,
                      SwitchStatement, ThrowStatement, TryStatement, WhileStatement,
                      YieldStatement, StatementList, VariableDeclaratorList)
from ...nodes import Program
from ...nodes import TypeIdentifier, DimensionSpecifier, TypeIdentifierList
from ...nodes import get_assignment_op, get_binary_op, get_unary_op, get_update_op
from ...nodes import node_factory


def convert_program(node: tree_sitter.Node) -> Program:
    assert node.type == 'program'
    stmts = []
    for ch in node.children:
        stmts.append(convert_statement(ch))
    return node_factory.create_program(node_factory.create_statement_list(stmts))


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
        'update_expression': convert_update_expr,
        'object_creation_expression': convert_new_expr,
        'cast_expression': convert_cast_expr,
        'instanceof_expression': convert_instanceof_expr,
        'ternary_expression': convert_ternary_expr,
        'this': convert_this_expr,
    }

    return expr_convertors[node.type](node)


def convert_statement(node: tree_sitter.Node) -> Statement:
    stmt_convertors = {
        ';': convert_empty_stmt,
        'local_variable_declaration': convert_local_variable_declaration,
        'expression_statement': convert_expression_stmt,
        'empty_statement': convert_empty_stmt,
        'block': convert_block_stmt,
        'for_statement': convert_for_stmt,
        'while_statement': convert_while_stmt,
    }

    return stmt_convertors[node.type](node)


def convert_type(node: tree_sitter.Node) -> TypeIdentifier:
    type_convertors = {
        'array_type': convert_array_type,
        'void_type': convert_simple_type,
        'integral_type': convert_simple_type,
        'floating_point_type': convert_simple_type,
        'boolean_type': convert_simple_type,
        'scoped_type_identifier': convert_simple_type,
        'generic_type': convert_simple_type,
        'type_identifier': convert_simple_type,
        'identifier': convert_simple_type,
    }

    return type_convertors[node.type](node)


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


def convert_cast_expr(node: tree_sitter.Node) -> CastExpression:
    # TODO: type intersections
    type_node = node.child_by_field_name('type')
    value_node = node.child_by_field_name('value')

    type_id = convert_type(type_node)
    value_expr = convert_expression(value_node)
    return node_factory.create_cast_expr(type_id, value_expr)


def convert_field_access(node: tree_sitter.Node) -> FieldAccess:
    if node.child_count != 3:
        raise RuntimeError(f'field access with {node.child_count} children')

    obj_expr = convert_expression(node.child_by_field_name('object'))
    name_expr = convert_expression(node.child_by_field_name('field'))
    return node_factory.create_field_access(obj_expr, name_expr)


def convert_argument_list(node: tree_sitter.Node) -> ExpressionList:
    args = []
    for ch in node.children[1:-1]:
        # skip parenthesis and comma sep
        if ch.type == ',':
            continue
        args.append(convert_expression(ch))
    return node_factory.create_expression_list(args)


def convert_call_expr(node: tree_sitter.Node) -> CallExpression:
    if node.child_count != 2 and node.child_count != 4:
        raise RuntimeError(f'call expr with {node.child_count} children')

    arg_node = node.child_by_field_name('arguments')
    args = convert_argument_list(arg_node)

    name_expr = convert_expression(node.child_by_field_name('name'))
    obj_node = node.child_by_field_name('object')
    if obj_node is not None:
        obj_expr = convert_expression(obj_node)
        callee_expr = node_factory.create_field_access(obj_expr, name_expr)
    else:
        callee_expr = name_expr

    return node_factory.create_call_expr(callee_expr, args)


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
    # TODO: type_argument
    # type_arg_node = node.child_by_field_name('type_arguments')
    type_node = node.child_by_field_name('type')
    args_node = node.child_by_field_name('arguments')

    type_id = convert_type(type_node)
    args = convert_argument_list(args_node)
    return node_factory.create_new_expr(type_id, args)


def convert_instanceof_expr(node: tree_sitter.Node) -> InstanceofExpression:
    # TODO: name field, final modifier (children[2])
    # name_node = node.child_by_field_name('name')
    left_node = node.child_by_field_name('left')
    right_node = node.child_by_field_name('right')

    left = convert_expression(left_node)
    right = convert_type(right_node)
    return node_factory.create_instanceof_expr(left, right)


def convert_ternary_expr(node: tree_sitter.Node) -> TernaryExpression:
    condition_node = node.child_by_field_name('condition')
    consequence_node = node.child_by_field_name('consequence')
    alternate_node = node.child_by_field_name('alternative')

    condition = convert_expression(condition_node)
    consequence = convert_expression(consequence_node)
    alternate = convert_expression(alternate_node)
    return node_factory.create_ternary_expr(condition, consequence, alternate)


def convert_this_expr(node: tree_sitter.Node) -> ThisExpression:
    return node_factory.create_this_expr()


def convert_dimension(node: tree_sitter.Node) -> DimensionSpecifier:
    return node_factory.create_dimension_specifier(node.text.decode().count('['))


def convert_simple_type(node: tree_sitter.Node) -> TypeIdentifier:
    return node_factory.create_type_identifier(node.text.decode())


def convert_array_type(node: tree_sitter.Node) -> TypeIdentifier:
    element_ty = convert_type(node.child_by_field_name('element'))
    dimensions = convert_dimension(node.child_by_field_name('dimensions'))
    return node_factory.create_array_type(element_ty, dimensions)


def convert_expression_stmt(node: tree_sitter.Node) -> ExpressionStatement:
    expr = convert_expression(node.children[0])
    return node_factory.create_expression_stmt(expr)


def convert_variable_declarator(node: tree_sitter.Node) -> VariableDeclarator:
    name_node = node.child_by_field_name('name')
    dim_node = node.child_by_field_name('dimensions')
    value_node = node.child_by_field_name('value')

    name_expr = convert_expression(name_node)
    dim_expr = convert_dimension(dim_node) if dim_node is not None else None
    value_expr = convert_expression(value_node) if value_node is not None else None
    return node_factory.create_variable_declarator(name_expr, dim_expr, value_expr)


def convert_local_variable_declaration(
        node: tree_sitter.Node) -> LocalVariableDeclaration:
    if node.children[0].type == 'modifiers':
        raise NotImplementedError('modifiers in local var decl')

    ty = convert_type(node.child_by_field_name('type'))
    declarators = []
    for decl_node in node.children_by_field_name('declarator'):
        declarators.append(convert_variable_declarator(decl_node))
    declarators = node_factory.create_variable_declarator_list(declarators)

    return node_factory.create_local_var_decl(ty, declarators)


def convert_empty_stmt(node: tree_sitter.Node) -> EmptyStatement:
    return node_factory.create_empty_stmt()


def convert_block_stmt(node: tree_sitter.Node) -> BlockStatement:
    stmts = []
    for stmt_node in node.children[1:-1]:
        stmts.append(convert_statement(stmt_node))
    stmts = node_factory.create_statement_list(stmts)
    return node_factory.create_block_stmt(stmts)


def convert_for_stmt(node: tree_sitter.Node) -> ForStatement:
    init_nodes = node.children_by_field_name('init')
    cond_node = node.child_by_field_name('condition')
    update_node = node.children_by_field_name('update')
    body_node = node.child_by_field_name('body')

    body = convert_statement(body_node)
    if len(init_nodes) == 0:
        init = None
    else:
        if init_nodes[0].type == 'local_variable_declaration':
            assert len(init_nodes) == 1
            init = convert_local_variable_declaration(init_nodes[0])
        else:
            init = [convert_expression(init_node) for init_node in init_nodes]
            init = node_factory.create_expression_list(init)
    cond = convert_expression(cond_node) if cond_node is not None else None
    if len(update_node) == 0:
        update = None
    else:
        update = [convert_expression(update) for update in update_node]
        update = node_factory.create_expression_list(update)
    return node_factory.create_for_stmt(body, init, cond, update)


def convert_while_stmt(node: tree_sitter.Node) -> WhileStatement:
    cond_node = node.child_by_field_name('condition')
    assert cond_node.child_count == 3, 'while condition with != 3 children'
    cond_node = cond_node.children[1]
    body_node = node.child_by_field_name('body')

    cond = convert_expression(cond_node)
    body = convert_statement(body_node)
    return node_factory.create_while_stmt(cond, body)
