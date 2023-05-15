from typing import List
from mutable_tree.node.node import Node
from ..node import NodeType
from .expression import Expression
from .expression import is_primary_expression


class FieldAccess(Expression):

    def __init__(self, node_type: NodeType, object: Expression, field: Expression):
        super().__init__(node_type)
        self.object = object
        self.field = field
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.FIELD_ACCESS:
            raise TypeError(f'Invalid type: {self.node_type} for FieldAccess')
        if not is_primary_expression(self.object):
            raise TypeError(
                f'Invalid type: {self.object.node_type} for field access object')
        f_nt = self.field.node_type
        if (f_nt != NodeType.IDENTIFIER and f_nt != NodeType.THIS_EXPR):
            raise TypeError(f'Invalid type: {f_nt} for field access field')

    def to_string(self) -> str:
        return f'{self.object.to_string()}.{self.field.to_string()}'

    def get_children(self) -> List[Node]:
        return [self.object, self.field]
