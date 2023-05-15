from ..node import Node, NodeType
from ..utils import throw_invalid_type


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
