from ..node import Node, NodeType
from .statement import Statement
from .statement import is_statement
from ..expressions import Expression, Identifier
from ..types import TypeIdentifier
from ..miscs import ModifierList
from ..expressions import is_expression
from ..utils import throw_invalid_type
from typing import List, Optional


class ForInStatement(Statement):

    def __init__(self,
                 node_type: NodeType,
                 type_identifier: TypeIdentifier,
                 iterator: Identifier,
                 iterable: Expression,
                 body: Statement,
                 modifiers: Optional[ModifierList] = None):
        super().__init__(node_type)
        self.it_type = type_identifier
        self.iter = iterator
        self.iterable = iterable
        self.body = body
        self.modifiers = modifiers
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.FOR_IN_STMT:
            throw_invalid_type(self.node_type, self)
        if self.it_type.node_type != NodeType.TYPE_IDENTIFIER:
            throw_invalid_type(self.it_type.node_type, self, attr='it_type')
        if self.iter.node_type != NodeType.IDENTIFIER:
            throw_invalid_type(self.iter.node_type, self, attr='iter')
        if not is_expression(self.iterable):
            throw_invalid_type(self.iterable.node_type, self, attr='iterable')
        if not is_statement(self.body):
            throw_invalid_type(self.body.node_type, self, attr='body')
        if (self.modifiers is not None
                and self.modifiers.node_type != NodeType.MODIFIER_LIST):
            throw_invalid_type(self.modifiers.node_type, self, attr='modifiers')

    def to_string(self) -> str:
        it_type_str = self.it_type.to_string()
        iter_str = self.iter.to_string()
        iterable_str = self.iterable.to_string()
        body_str = self.body.to_string()

        if self.modifiers is not None:
            modifier_str = self.modifiers.to_string()
            return (f'for ({modifier_str} {it_type_str} {iter_str} : {iterable_str})\n'
                    f'{body_str}')
        else:
            return f'for ({it_type_str} {iter_str} : {iterable_str})\n{body_str}'

    def get_children(self) -> List[Node]:
        if self.modifiers is not None:
            return [self.modifiers, self.it_type, self.iter, self.iterable, self.body]
        else:
            return [self.it_type, self.iter, self.iterable, self.body]

    def get_children_names(self) -> List[str]:
        return ['modifiers', 'it_type', 'iter', 'iterable', 'body']
