from ..node import Node, NodeType
from .dimension_specifier import DimensionSpecifier
from typing import Optional


class TypeIdentifier(Node):

    def __init__(self, node_type: NodeType, type_identifier: str,
                 dimension: Optional[DimensionSpecifier]):
        super().__init__(node_type)
        self.type_identifier = type_identifier
        self.dimension = dimension

    def _check_types(self):
        if self.node_type != NodeType.TYPE_IDENTIFIER:
            raise TypeError(f'Invalid type: {self.node_type} for TypeIdentifier.')

    def to_string(self) -> str:
        if self.dimension is not None:
            return f'{self.type_identifier}{self.dimension.to_string()}'
        else:
            return self.type_identifier
