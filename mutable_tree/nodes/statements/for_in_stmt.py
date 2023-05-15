from ..node import Node, NodeType
from .statement import Statement
from .statement import is_statement
from ..expressions import Expression, Identifier
from ..types import TypeIdentifier
from ..expressions import is_expression
from typing import List


class ForInStatement(Statement):

    def __init__(self, node_type: NodeType, type_identifier: TypeIdentifier,
                 iterator: Identifier, iterable: Expression, body: Statement):
        super().__init__(node_type)
        self.it_type = type_identifier
        self.iter = iterator
        self.iterable = iterable
        self.body = body
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.FOR_IN_STMT:
            raise TypeError(f'Invalid type: {self.node_type} for ForInStatement')
        if self.it_type.node_type != NodeType.TYPE_IDENTIFIER:
            raise TypeError(f'Invalid type: {self.it_type.node_type} for for-in type')
        if self.iter.node_type != NodeType.IDENTIFIER:
            raise TypeError(f'Invalid type: {self.iter.node_type} for for-in iterator')
        if not is_expression(self.iterable):
            raise TypeError(
                f'Invalid type: {self.iterable.node_type} for for-in iterable')
        if not is_statement(self.body):
            raise TypeError(f'Invalid type: {self.body.node_type} for for-in body')

    def to_string(self) -> str:
        it_type_str = self.it_type.to_string()
        iter_str = self.iter.to_string()
        iterable_str = self.iterable.to_string()
        body_str = self.body.to_string()
        return f'for ({it_type_str} {iter_str} : {iterable_str})\n{body_str}'

    def get_children(self) -> List[Node]:
        return [self.it_type, self.iter, self.iterable, self.body]

    def get_children_names(self) -> List[str]:
        return ['it_type', 'iter', 'iterable', 'body']
