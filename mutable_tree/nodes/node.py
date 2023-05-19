from enum import Enum
from typing import List


# types
class NodeType(Enum):
    # top-level
    PROGRAM = 'Program'

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
    ARRAY_EXPR = 'ArrayExpression'
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
    EMPTY_STMT = 'EmptyStatement'
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
    TRY_WITH_RESOURCES_STMT = 'TryWithResourcesStatement'
    WHILE_STMT = 'WhileStatement'
    YIELD_STMT = 'YieldStatement'

    # declarations & definitions (are also statements)
    FUNC_DECLARATOR = 'FunctionDeclarator'
    FUNC_DECLARATION = 'FunctionDeclaration'

    # miscs
    DIMENSION_SPECIFIER = 'DimensionSpecifier'
    VARIABLE_DECLARATOR = 'VariableDeclarator'
    SWITCH_CASE = 'SwitchCase'
    CATCH_CLAUSE = 'CatchClause'
    FINALLY_CLAUSE = 'FinallyClause'
    EXPRESSION_LIST = 'ExpressionList'
    STATEMENT_LIST = 'StatementList'
    VARIABLE_DECLARATOR_LIST = 'VariableDeclaratorList'
    SWITCH_CASE_LIST = 'SwitchCaseList'
    TYPE_IDENTIFIER = 'TypeIdentifier'
    TYPE_IDENTIFIER_LIST = 'TypeIdentifierList'
    TRY_HANDLERS = 'TryHandlers'
    TRY_RESOURCE = 'TryResource'
    TRY_RESOURCE_LIST = 'TryResourceList'

    MODIFIER = 'Modifier'
    MODIFIER_LIST = 'ModifierList'
    FORMAL_PARAMETER = 'FormalParameter'
    FORMAL_PARAMETER_LIST = 'FormalParameterList'


class Node:
    node_type: NodeType

    def __init__(self, node_type: NodeType):
        self.node_type = node_type

    def _check_types(self):
        raise NotImplementedError('Base class Node should never be initialized')

    def to_string(self) -> str:
        raise NotImplementedError()

    def get_children(self) -> List['Node']:
        raise NotImplementedError()

    def get_children_names(self) -> List[str]:
        raise NotImplementedError()

    def get_child_at(self, attr: str) -> 'Node':
        return getattr(self, attr)

    def set_child_at(self, attr: str, value: 'Node'):
        if not hasattr(self, attr):
            raise AttributeError(f'{type(self).__name__} does not have attribute {attr}')
        setattr(self, attr, value)


class NodeList(Node):
    node_list: List[Node]

    def __init__(self, node_type: NodeType):
        super().__init__(node_type)

    def get_children(self) -> List[Node]:
        return self.node_list

    def get_children_names(self) -> List[int]:
        return list(range(len(self.node_list)))

    def get_child_at(self, index: int) -> Node:
        return self.node_list[index]

    def set_child_at(self, index: int, value: Node):
        self.node_list[index] = value

    def replace_child_at(self, index: int, values: List[Node]):
        self.node_list[index:index + 1] = values
