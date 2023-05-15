from ..node import Node, NodeType
from .statement import Statement
from ..expressions import Expression, Identifier
from ..types import TypeIdentifier, DimensionSpecifier
from ..expressions import is_expression
from ..utils import throw_invalid_type
from typing import List, Optional


class VariableDeclarator(Node):

    def __init__(self,
                 node_type: NodeType,
                 name: Identifier,
                 dimensions: Optional[DimensionSpecifier] = None,
                 value: Optional[Expression] = None):
        super().__init__(node_type)
        self.name = name
        self.dimensions = dimensions
        self.value = value
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.VARIABLE_DECLARATOR:
            throw_invalid_type(self.node_type, self)
        if (self.dimensions is not None and
                self.dimensions.node_type != NodeType.DIMENSION_SPECIFIER):
            throw_invalid_type(self.dimensions.node_type, self, attr='dimensions')
        if self.value is not None and not is_expression(self.value):
            throw_invalid_type(self.value.node_type, self, attr='value')

    def to_string(self) -> str:
        declarator_id = self.name.to_string()
        if self.dimensions is not None:
            declarator_id += self.dimensions.to_string()

        if self.value is not None:
            return f'{declarator_id} = {self.value.to_string()}'
        else:
            return declarator_id

    def get_children(self) -> List[Node]:
        children = [self.name]
        if self.dimensions is not None:
            children.append(self.dimensions)
        if self.value is not None:
            children.append(self.value)
        return children


class LocalVariableDeclaration(Statement):

    def __init__(self, node_type: NodeType, type_identifier: TypeIdentifier,
                 declarators: List[VariableDeclarator]):
        super().__init__(node_type)
        self.type = type_identifier
        self.declarators = declarators
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.LOCAL_VAR_DECL:
            throw_invalid_type(self.node_type, self)
        for i, decl in enumerate(self.declarators):
            if decl.node_type != NodeType.VARIABLE_DECLARATOR:
                throw_invalid_type(decl.node_type, self, attr=f'declarator#{i}')

    def to_string(self) -> str:
        decl_strs = ', '.join(decl.to_string() for decl in self.declarators)
        return f'{self.type.to_string()} {decl_strs};'

    def get_children(self) -> List[Node]:
        return [self.type] + self.declarators
