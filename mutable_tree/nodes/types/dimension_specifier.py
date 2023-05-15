from ..node import Node, NodeType
from ..utils import throw_invalid_type
from typing import List


class DimensionSpecifier(Node):

    def __init__(self, node_type: NodeType, dims: int):
        super().__init__(node_type)
        self.dims = dims
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.DIMENSION_SPECIFIER:
            throw_invalid_type(self.node_type, self)

    def to_string(self) -> str:
        return '[]' * self.dims

    def get_children(self) -> List[Node]:
        return []

    def get_children_names(self) -> List[str]:
        return []