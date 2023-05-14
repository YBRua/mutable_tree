from enum import Enum
from typing import List, Optional


class NodeType(Enum):
    # types
    TYPE_IDENTIFIER = 'TypeIdentifier'

    # expressions
    ASSIGNMENT_EXPR = 'AssignmentExpression'
    BINARY_EXPR = 'BinaryExpression'
    INSTANCEOF_EXPR = 'InstanceofExpression'
    LAMBDA_EXPR = 'LambdaExpression'
    TERNARY_EXPR = 'TernaryExpression'
    UPDATE_EXPR = 'UpdateExpression'
    UNARY_EXPR = 'UnaryExpression'
    CAST_EXPR = 'CastExpression'  # NOT IMPLEMENTED

    # primary expressions
    LITERAL = 'Literal'
    IDENTIFIER = 'Identifier'
    ARRAY_EXPRESSION = 'ArrayExpression'
    THIS_EXPR = 'ThisExpression'
    PARENTHESIZED_EXPR = 'ParenthesizedExpression'
    NEW_EXPR = 'NewExpression'
    CALL_EXPR = 'CallExpression'
    FIELD_ACCESS = 'FieldAccess'
    ARRAY_ACCESS = 'ArrayAccess'

    # statements
    ASSERT_STMT = 'AssertStatement'
    BLOCK_STMT = 'BlockStatement'
    BREAK_STMT = 'BreakStatement'
    CONTINUE_STMT = 'ContinueStatement'
    DECLARATION_STMT = 'DeclarationStatement'  # NOT IMPLEMENTED
    DO_STMT = 'DoStatement'
    EXPRESSION_STMT = 'ExpressionStatement'
    FOR_STMT = 'ForStatement'
    FOR_IN_STMT = 'ForInStatement'
    IF_STMT = 'IfStatement'
    LABELED_STMT = 'LabeledStatement'
    LOCAL_VAR_DECL = 'LocalVariableDeclaration'
    RETURN_STMT = 'ReturnStatement'
    SWITCH_STMT = 'SwitchStatement'
    SYNC_STMT = 'SynchronizedStatement'
    THROW_STMT = 'ThrowStatement'
    TRY_STMT = 'TryStatement'
    WHILE_STMT = 'WhileStatement'
    YIELD_STMT = 'YieldStatement'

    # miscs
    DIMENSION_SPECIFIER = 'DimensionSpecifier'
    VARIABLE_DECLARATOR = 'VariableDeclarator'
    SWITCH_CASE = 'SwitchCase'


class Node:
    node_type: NodeType

    def __init__(self, node_type: NodeType):
        self.node_type = node_type

    def _check_types(self):
        raise NotImplementedError('Base class Node should never be initialized')

    def to_string(self) -> str:
        raise NotImplementedError()
