from ..node import Node, NodeType, NodeList
from .statement import Statement
from .block_stmt import BlockStatement
from ..expressions import Identifier
from ..types import TypeIdentifierList
from ..utils import throw_invalid_type
from typing import List, Optional


class CatchClause(Node):

    def __init__(self, node_type: NodeType, catch_types: TypeIdentifierList,
                 exception: Identifier, body: BlockStatement):
        super().__init__(node_type)
        self.catch_types = catch_types
        self.exception = exception
        self.body = body
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.CATCH_CLAUSE:
            throw_invalid_type(self.node_type, self)
        if self.exception.node_type != NodeType.IDENTIFIER:
            throw_invalid_type(self.exception.node_type, self, attr='exception')
        if self.body.node_type != NodeType.BLOCK_STMT:
            throw_invalid_type(self.body.node_type, self, attr='body')
        if self.catch_types.node_type != NodeType.TYPE_IDENTIFIER_LIST:
            throw_invalid_type(self.catch_types.node_type, self, attr='catch_types')

    def to_string(self) -> str:
        catch_types_str = ' | '.join(
            [ty.to_string() for ty in self.catch_types.get_children()])
        exception_str = self.exception.to_string()
        body_str = self.body.to_string()
        return f'catch ({catch_types_str} {exception_str}) {body_str}'

    def get_children(self) -> List[Node]:
        return [self.catch_types, self.exception, self.body]

    def get_children_names(self) -> List[str]:
        return ['catch_types', 'exception', 'body']


class TryHandlers(NodeList):
    node_list: List[CatchClause]

    def __init__(self, node_type: NodeType, handlers: List[CatchClause]):
        super().__init__(node_type)
        self.node_list = handlers

    def _check_types(self):
        if self.node_type != NodeType.TRY_HANDLERS:
            throw_invalid_type(self.node_type, self)
        for i, handler in enumerate(self.node_list):
            if handler.node_type != NodeType.CATCH_CLAUSE:
                throw_invalid_type(handler.node_type, self, attr=f'handler#{i}')


class FinallyClause(Node):

    def __init__(self, node_type: NodeType, body: BlockStatement):
        super().__init__(node_type)
        self.body = body
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.FINALLY_CLAUSE:
            throw_invalid_type(self.node_type, self)
        if self.body.node_type != NodeType.BLOCK_STMT:
            throw_invalid_type(self.body.node_type, self, attr='body')

    def to_string(self) -> str:
        body_str = self.body.to_string()
        return f'finally \n{body_str}\n'

    def get_children_names(self) -> List[str]:
        return ['body']


class TryStatement(Statement):

    def __init__(self,
                 node_type: NodeType,
                 body: BlockStatement,
                 handlers: TryHandlers,
                 finalizer: Optional[FinallyClause] = None):
        super().__init__(node_type)
        self.body = body
        self.handlers = handlers
        self.finalizer = finalizer
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.TRY_STMT:
            throw_invalid_type(self.node_type, self)
        if self.body.node_type != NodeType.BLOCK_STMT:
            throw_invalid_type(self.body.node_type, self, attr='body')
        if (self.finalizer is not None
                and self.finalizer.node_type != NodeType.FINALLY_CLAUSE):
            throw_invalid_type(self.finalizer.node_type, self, attr='finalizer')
        if self.handlers.node_type != NodeType.TRY_HANDLERS:
            throw_invalid_type(self.handlers.node_type, self, attr='handlers')

    def to_string(self) -> str:
        body_str = self.body.to_string()
        handlers_str = '\n'.join(
            [handler.to_string() for handler in self.handlers.get_children()])
        if self.finalizer is not None:
            finalizer_str = self.finalizer.to_string()
            return f'try {body_str}\n{handlers_str}\n{finalizer_str}'
        else:
            return f'try {body_str}\n{handlers_str}'

    def get_children_names(self) -> List[str]:
        return ['body', 'handlers', 'finalizer']
