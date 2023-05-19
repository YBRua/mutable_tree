from ..node import Node, NodeType, NodeList
from .statement import Statement
from ..miscs import ModifierList
from ..expressions import Expression, Identifier
from ..types import TypeIdentifier, Dimensions
from ..expressions import is_expression
from ..utils import throw_invalid_type
from typing import List, Optional


class VariableDeclarator(Node):

    def __init__(self,
                 node_type: NodeType,
                 name: Identifier,
                 dimensions: Optional[Dimensions] = None,
                 value: Optional[Expression] = None):
        super().__init__(node_type)
        self.name = name
        self.dimensions = dimensions
        self.value = value
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.VARIABLE_DECLARATOR:
            throw_invalid_type(self.node_type, self)
        if (self.dimensions is not None
                and self.dimensions.node_type != NodeType.DIMENSIONS):
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

    def get_children_names(self) -> List[str]:
        return ['name', 'dimensions', 'value']


class VariableDeclaratorList(NodeList):
    node_list: List[VariableDeclarator]

    def __init__(self, node_type: NodeType, declarators: List[VariableDeclarator]):
        super().__init__(node_type)
        self.node_list = declarators
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.VARIABLE_DECLARATOR_LIST:
            throw_invalid_type(self.node_type, self)
        for i, decl in enumerate(self.node_list):
            if decl.node_type != NodeType.VARIABLE_DECLARATOR:
                throw_invalid_type(decl.node_type, self, attr=f'declarator#{i}')


class LocalVariableDeclaration(Statement):

    def __init__(self,
                 node_type: NodeType,
                 type_identifier: TypeIdentifier,
                 declarators: VariableDeclaratorList,
                 modifiers: Optional[ModifierList] = None):
        super().__init__(node_type)
        self.type = type_identifier
        self.declarators = declarators
        self.modifiers = modifiers
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.LOCAL_VAR_DECL:
            throw_invalid_type(self.node_type, self)
        if self.declarators.node_type != NodeType.VARIABLE_DECLARATOR_LIST:
            throw_invalid_type(self.declarators.node_type, self, attr='declarators')
        if (self.modifiers is not None
                and self.modifiers.node_type != NodeType.MODIFIER_LIST):
            throw_invalid_type(self.modifiers.node_type, self, attr='modifiers')

    def to_string(self) -> str:
        decl_strs = ', '.join(decl.to_string()
                              for decl in self.declarators.get_children())
        res = f'{self.type.to_string()} {decl_strs};'
        if self.modifiers is not None:
            res = f'{self.modifiers.to_string()} {res}'
        return res

    def get_children(self) -> List[Node]:
        if self.modifiers is not None:
            return [self.modifiers, self.type, self.declarators]
        else:
            return [self.type, self.declarators]

    def get_children_names(self) -> List[str]:
        return ['modifiers', 'type', 'declarators']
