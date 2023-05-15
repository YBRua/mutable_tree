from ..node import NodeType
from .statement import Statement
from ..utils import throw_invalid_type


class EmptyStatement(Statement):

    def __init__(self, node_type: NodeType):
        super().__init__(node_type)
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.EMPTY_STMT:
            throw_invalid_type(self.node_type, self)

    def to_string(self) -> str:
        return ';'
