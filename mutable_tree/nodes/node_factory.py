from .node import NodeType
from .program import Program
from .expressions import Expression
from .expressions import BinaryOps, UnaryOps, UpdateOps, AssignmentOps
from .expressions import (ArrayAccess, ArrayExpression, ArrayCreationExpression,
                          AssignmentExpression, BinaryExpression, CallExpression,
                          CastExpression, FieldAccess, Identifier, InstanceofExpression,
                          Literal, NewExpression, TernaryExpression, ThisExpression,
                          UnaryExpression, UpdateExpression, PrimaryExpression,
                          ParenthesizedExpression, ExpressionList)
from .statements import Statement
from .statements import (AssertStatement, BlockStatement, BreakStatement,
                         ContinueStatement, DoStatement, EmptyStatement,
                         ExpressionStatement, ForInStatement, ForStatement, IfStatement,
                         LabeledStatement, LocalVariableDeclaration, VariableDeclarator,
                         ReturnStatement, SwitchCase, SwitchCaseList, SwitchStatement,
                         ThrowStatement, TryStatement, TryHandlers, CatchClause,
                         FinallyClause, WhileStatement, YieldStatement, StatementList,
                         VariableDeclaratorList, TryResource, TryResourceList,
                         TryWithResourcesStatement)
from .statements import (FormalParameter, FormalParameterList, FunctionDeclarator,
                         FunctionDeclaration)
from .miscs import Modifier, ModifierList
from .statements.for_stmt import ForInit
from .types import TypeIdentifier, TypeIdentifierList, DimensionSpecifier, Dimensions

from typing import Union, Optional, List

# TOP LEVEL


def create_program(stmts: StatementList) -> Program:
    return Program(NodeType.PROGRAM, stmts)


# TYPES


def create_array_type(type_identifier: TypeIdentifier,
                      dimension: Dimensions) -> TypeIdentifier:
    type_identifier.dimension = dimension
    return type_identifier


def create_type_identifier(
    name: str,
    dimension: Optional[Dimensions] = None,
) -> TypeIdentifier:
    return TypeIdentifier(NodeType.TYPE_IDENTIFIER, name, dimension)


def create_dimension_specifier(expr: Optional[Expression] = None) -> DimensionSpecifier:
    return DimensionSpecifier(NodeType.DIMENSION_SPECIFIER, expr)


def create_dimensions(dims: List[DimensionSpecifier]) -> Dimensions:
    return Dimensions(NodeType.DIMENSIONS, dims)


# EXPRESSIONS


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


def create_array_expr(elements: ExpressionList) -> ArrayExpression:
    return ArrayExpression(NodeType.ARRAY_EXPR, elements)


def create_call_expr(callee: PrimaryExpression, args: ExpressionList) -> CallExpression:
    return CallExpression(NodeType.CALL_EXPR, callee, args)


def create_cast_expr(type_name: TypeIdentifier, expr: Expression) -> CastExpression:
    return CastExpression(NodeType.CAST_EXPR, type_name, expr)


def create_field_access(obj: PrimaryExpression, field: Identifier) -> FieldAccess:
    return FieldAccess(NodeType.FIELD_ACCESS, obj, field)


def create_instanceof_expr(expr: Expression,
                           type_name: TypeIdentifier) -> InstanceofExpression:
    return InstanceofExpression(NodeType.INSTANCEOF_EXPR, expr, type_name)


def create_new_expr(type_name: TypeIdentifier, args: ExpressionList) -> NewExpression:
    return NewExpression(NodeType.NEW_EXPR, type_name, args)


def create_array_creation_expr(
        type_name: TypeIdentifier,
        dimensions: Dimensions,
        initializer: Optional[ArrayExpression] = None) -> ArrayCreationExpression:
    return ArrayCreationExpression(NodeType.ARRAY_CREATION_EXPR, type_name, dimensions,
                                   initializer)


def create_ternary_expr(condition: Expression, consequence: Expression,
                        alternate: Expression) -> TernaryExpression:
    return TernaryExpression(NodeType.TERNARY_EXPR, condition, consequence, alternate)


def create_this_expr() -> ThisExpression:
    return ThisExpression(NodeType.THIS_EXPR)


def create_parenthesized_expr(expr: Expression) -> Expression:
    return ParenthesizedExpression(NodeType.PARENTHESIZED_EXPR, expr)


# STATEMENTS


def create_empty_stmt() -> EmptyStatement:
    return EmptyStatement(NodeType.EMPTY_STMT)


def create_expression_stmt(expr: Expression) -> ExpressionStatement:
    return ExpressionStatement(NodeType.EXPRESSION_STMT, expr)


def create_for_stmt(
    body: Statement,
    init: Optional[ForInit] = None,
    condition: Optional[Expression] = None,
    update: Optional[ExpressionList] = None,
) -> ForStatement:
    return ForStatement(NodeType.FOR_STMT, body, init, condition, update)


def create_while_stmt(condition: Expression, body: Statement) -> WhileStatement:
    return WhileStatement(NodeType.WHILE_STMT, condition, body)


def create_block_stmt(statements: StatementList) -> BlockStatement:
    return BlockStatement(NodeType.BLOCK_STMT, statements)


def create_variable_declarator(name: Identifier,
                               dimension: Optional[Dimensions] = None,
                               value: Optional[Expression] = None) -> VariableDeclarator:
    return VariableDeclarator(NodeType.VARIABLE_DECLARATOR, name, dimension, value)


def create_local_var_decl(
        type_name: TypeIdentifier,
        declarators: VariableDeclaratorList,
        modifiers: Optional[ModifierList] = None) -> LocalVariableDeclaration:
    return LocalVariableDeclaration(NodeType.LOCAL_VAR_DECL, type_name, declarators,
                                    modifiers)


def create_assert_stmt(condition: Expression,
                       message: Optional[Expression] = None) -> AssertStatement:
    return AssertStatement(NodeType.ASSERT_STMT, condition, message)


def create_break_stmt(label: Optional[Identifier] = None) -> BreakStatement:
    return BreakStatement(NodeType.BREAK_STMT, label)


def create_continue_stmt(label: Optional[Identifier] = None) -> ContinueStatement:
    return ContinueStatement(NodeType.CONTINUE_STMT, label)


def create_do_stmt(condition: Expression, body: Statement) -> DoStatement:
    return DoStatement(NodeType.DO_STMT, body, condition)


def create_for_in_stmt(
    type_id: TypeIdentifier,
    iterator: Identifier,
    iterable: Expression,
    body: Statement,
) -> ForInStatement:
    return ForInStatement(NodeType.FOR_IN_STMT, type_id, iterator, iterable, body)


def create_if_stmt(
    condition: Expression,
    consequence: Statement,
    alternate: Optional[Statement] = None,
) -> IfStatement:
    return IfStatement(NodeType.IF_STMT, condition, consequence, alternate)


def create_labeled_stmt(label: Identifier, stmt: Statement) -> LabeledStatement:
    return LabeledStatement(NodeType.LABELED_STMT, label, stmt)


def create_return_stmt(value: Optional[Expression] = None) -> ReturnStatement:
    return ReturnStatement(NodeType.RETURN_STMT, value)


def create_switch_case(
    stmts: StatementList,
    case: Optional[Expression] = None,
) -> SwitchCase:
    return SwitchCase(NodeType.SWITCH_CASE, stmts, case)


def create_switch_case_list(cases: List[SwitchCase]) -> SwitchCaseList:
    return SwitchCaseList(NodeType.SWITCH_CASE_LIST, cases)


def create_switch_stmt(
    condition: Expression,
    cases: SwitchCaseList,
) -> SwitchStatement:
    return SwitchStatement(NodeType.SWITCH_STMT, condition, cases)


def create_throw_stmt(expr: Expression) -> ThrowStatement:
    return ThrowStatement(NodeType.THROW_STMT, expr)


def create_yield_stmt(expr: Expression) -> YieldStatement:
    return YieldStatement(NodeType.YIELD_STMT, expr)


def create_catch_clause(
    exception_types: TypeIdentifierList,
    exception: Identifier,
    body: BlockStatement,
) -> CatchClause:
    return CatchClause(NodeType.CATCH_CLAUSE, exception_types, exception, body)


def create_finally_clause(body: BlockStatement) -> FinallyClause:
    return FinallyClause(NodeType.FINALLY_CLAUSE, body)


def create_try_handlers(catch_clauses: List[CatchClause]) -> TryHandlers:
    return TryHandlers(NodeType.TRY_HANDLERS, catch_clauses)


def create_try_stmt(
    try_block: BlockStatement,
    handlers: TryHandlers,
    finally_clause: Optional[FinallyClause] = None,
) -> TryStatement:
    return TryStatement(NodeType.TRY_STMT, try_block, handlers, finally_clause)


def create_try_resource(
        resource: Union[Identifier, FieldAccess,
                        LocalVariableDeclaration]) -> TryResource:
    return TryResource(NodeType.TRY_RESOURCE, resource)


def create_try_resource_list(resources: List[TryResource]) -> TryResourceList:
    return TryResourceList(NodeType.TRY_RESOURCE_LIST, resources)


def create_try_with_resources_stmt(
    resources: TryResourceList,
    try_block: BlockStatement,
    handlers: TryHandlers,
    finally_clause: Optional[FinallyClause] = None,
) -> TryWithResourcesStatement:
    return TryWithResourcesStatement(NodeType.TRY_WITH_RESOURCES_STMT, resources,
                                     try_block, handlers, finally_clause)


# DECLARATIONS & DEFINITIONS


def create_formal_param(type_id: TypeIdentifier,
                        name: Identifier,
                        dimensions: Optional[Dimensions] = None,
                        modifiers: Optional[ModifierList] = None) -> FormalParameter:
    return FormalParameter(NodeType.FORMAL_PARAMETER, type_id, name, dimensions,
                           modifiers)


def create_formal_param_list(params: List[FormalParameter]) -> FormalParameterList:
    return FormalParameterList(NodeType.FORMAL_PARAMETER_LIST, params)


def create_func_declarator(
    return_type: TypeIdentifier,
    name: Identifier,
    params: FormalParameterList,
    dimensions: Optional[Dimensions] = None,
    throws: Optional[TypeIdentifierList] = None,
    modifiers: Optional[ModifierList] = None,
) -> FunctionDeclarator:
    return FunctionDeclarator(NodeType.FUNC_DECLARATOR, return_type, name, params,
                              dimensions, throws, modifiers)


def create_func_declaration(
        declarator: FunctionDeclarator,
        body: Union[BlockStatement, EmptyStatement]) -> FunctionDeclaration:
    return FunctionDeclaration(NodeType.FUNC_DECLARATION, declarator, body)


# MISCS


def create_type_identifier_list(type_ids: List[TypeIdentifier]) -> TypeIdentifierList:
    return TypeIdentifierList(NodeType.TYPE_IDENTIFIER_LIST, type_ids)


def create_expression_list(exprs: List[Expression]) -> ExpressionList:
    return ExpressionList(NodeType.EXPRESSION_LIST, exprs)


def create_statement_list(stmts: List[Statement]) -> StatementList:
    return StatementList(NodeType.STATEMENT_LIST, stmts)


def create_variable_declarator_list(
        declarators: List[VariableDeclarator]) -> VariableDeclaratorList:
    return VariableDeclaratorList(NodeType.VARIABLE_DECLARATOR_LIST, declarators)


def create_modifier(name: str) -> Modifier:
    return Modifier(NodeType.MODIFIER, name)


def create_modifier_list(modifiers: List[Modifier]) -> ModifierList:
    return ModifierList(NodeType.MODIFIER_LIST, modifiers)
