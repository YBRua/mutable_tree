from ..node import Node, NodeType
from ..utils import throw_invalid_type
from .type_identifier import TypeIdentifier
from typing import List


class TypeIdentifierList(Node):

    def __init__(self, node_type: NodeType, type_ids: List[TypeIdentifier]):
        super().__init__(node_type)
        self.type_ids = type_ids
        self._check_types

    def _check_types(self):
        if self.node_type != NodeType.TYPE_IDENTIFIER_LIST:
            throw_invalid_type(self.node_type, self)
        for i, type_id in enumerate(self.type_ids):
            if type_id.node_type != NodeType.TYPE_IDENTIFIER:
                throw_invalid_type(type_id.node_type, self, f'type_id#{i}')

    def get_children(self) -> List[Node]:
        return self.type_ids
