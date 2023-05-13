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
    THIS_EXPR = 'ThisExpression'
    PARENTHESIZED_EXPR = 'ParenthesizedExpression'
    NEW_EXPR = 'NewExpression'
    CALL_EXPR = 'CallExpression'
    FIELD_ACCESS = 'FieldAccess'
    ARRAY_ACCESS = 'ArrayAccess'

    # statements
    SWITCH_STMT = 'SwitchStatement'  # NOT IMPLEMENTED


class Node:
    children: Optional[List['Node']] = None
    node_type: NodeType

    def __init__(self, node_type: NodeType):
        self.node_type = node_type
        self._check_types()

    def _check_types(self):
        raise NotImplementedError('Base class Node should never be initialized')

    def to_string(self) -> str:
        raise NotImplementedError()
