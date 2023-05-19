from ..node import Node, NodeType, NodeList
from ..miscs import ModifierList
from ..expressions import Identifier
from ..types import TypeIdentifier, DimensionSpecifier
from ..utils import throw_invalid_type
from .statement import Statement
from .block_stmt import BlockStatement
from .empty_stmt import EmptyStatement
from typing import List, Optional, Union


class FormalParameter(Node):

    def __init__(self,
                 node_type: NodeType,
                 type_id: TypeIdentifier,
                 name: Identifier,
                 dimensions: Optional[DimensionSpecifier] = None,
                 modifiers: Optional[ModifierList] = None):
        super().__init__(node_type)
        self.type_id = type_id
        self.name = name
        self.dimensions = dimensions
        self.modifiers = modifiers
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.FORMAL_PARAMETER:
            throw_invalid_type(self.node_type, self)
        if self.type_id.node_type != NodeType.TYPE_IDENTIFIER:
            throw_invalid_type(self.type_id.node_type, self, attr='type_id')
        if self.name.node_type != NodeType.IDENTIFIER:
            throw_invalid_type(self.name.node_type, self, attr='name')
        if (self.dimensions is not None
                and self.dimensions.node_type != NodeType.DIMENSION_SPECIFIER):
            throw_invalid_type(self.dimensions.node_type, self, attr='dimensions')
        if (self.modifiers is not None
                and self.modifiers.node_type != NodeType.MODIFIER_LIST):
            throw_invalid_type(self.modifiers.node_type, self, attr='modifiers')

    def get_children(self) -> List[Node]:
        children = []
        if self.modifiers is not None:
            children.append(self.modifiers)
        children.append(self.type_id)
        children.append(self.name)
        if self.dimensions is not None:
            children.append(self.dimensions)

        return children

    def get_children_names(self) -> List[str]:
        return ['modifiers', 'type_id', 'name', 'dimensions']

    def to_string(self) -> str:
        res = ''
        if self.modifiers is not None:
            res += ' '.join(modifier.to_string()
                            for modifier in self.modifiers.get_children())
            res += ' '

        res += self.type_id.to_string()
        res += ' '
        res += self.name.to_string()
        if self.dimensions is not None:
            res += self.dimensions.to_string()
        return res


class FormalParameterList(NodeList):
    node_list: List[FormalParameter]

    def __init__(self, node_type: NodeType, parameters: List[FormalParameter]):
        super().__init__(node_type)
        self.node_list = parameters
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.FORMAL_PARAMETER_LIST:
            throw_invalid_type(self.node_type, self)
        for i, param in enumerate(self.node_list):
            if param.node_type != NodeType.FORMAL_PARAMETER:
                throw_invalid_type(param.node_type, self, attr=f'param#{i}')


class FunctionDeclarator(Node):

    def __init__(self,
                 node_type: NodeType,
                 return_type: TypeIdentifier,
                 name: Identifier,
                 parameters: FormalParameterList,
                 dimensions: Optional[DimensionSpecifier] = None):
        super().__init__(node_type)
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.dimensions = dimensions
        # TODO: dimensions for functions?
        if dimensions is not None:
            raise NotImplementedError('dimensions for functions are not supported yet')
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.FUNC_DECLARATOR:
            throw_invalid_type(self.node_type, self)
        if self.return_type.node_type != NodeType.TYPE_IDENTIFIER:
            throw_invalid_type(self.return_type.node_type, self, attr='return_type')
        if self.name.node_type != NodeType.IDENTIFIER:
            throw_invalid_type(self.name.node_type, self, attr='name')
        if self.parameters.node_type != NodeType.FORMAL_PARAMETER_LIST:
            throw_invalid_type(self.parameters.node_type, self, attr='parameters')
        if (self.dimensions is not None
                and self.dimensions.node_type != NodeType.DIMENSION_SPECIFIER):
            throw_invalid_type(self.dimensions.node_type, self, attr='dimensions')

    def to_string(self) -> str:
        ret_type_str = self.return_type.to_string()
        name_str = self.name.to_string()
        params_str = ', '.join(param.to_string()
                               for param in self.parameters.get_children())
        return f'{ret_type_str} {name_str}({params_str})'


class FunctionDeclaration(Statement):

    def __init__(self, node_type: NodeType, declarator: FunctionDeclarator,
                 body: Union[BlockStatement, EmptyStatement]):
        super().__init__(node_type)
        self.decorator = declarator
        self.body = body
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.FUNC_DECLARATION:
            throw_invalid_type(self.node_type, self)
        if self.decorator.node_type != NodeType.FUNC_DECLARATOR:
            throw_invalid_type(self.decorator.node_type, self, attr='decorator')
        if (self.body.node_type != NodeType.BLOCK_STMT
                and self.body.node_type != NodeType.EMPTY_STMT):
            throw_invalid_type(self.body.node_type, self, attr='body')

    def to_string(self) -> str:
        return f'{self.decorator.to_string()} {self.body.to_string()}'
