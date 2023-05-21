from ..node import Node, NodeType, NodeList
from ..miscs import ModifierList
from ..expressions import Identifier
from ..types import TypeIdentifier, Dimensions, TypeIdentifierList, TypeParameterList
from ..utils import throw_invalid_type
from .statement import Statement
from .local_var_decl import DeclaratorType
from .declarators import Declarator, is_declarator
from .block_stmt import BlockStatement
from .empty_stmt import EmptyStatement
from typing import List, Optional, Union


class FormalParameter(Node):
    pass


def is_formal_parameter(node: Node) -> bool:
    return isinstance(node, FormalParameter)


class InferredParameter(FormalParameter):

    def __init__(self, node_type: NodeType, decl: Declarator):
        super().__init__(node_type)
        self.declarator = decl
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.UNTYPED_PARAMETER:
            throw_invalid_type(self.node_type, self)
        if not is_declarator(self.declarator):
            throw_invalid_type(self.declarator.node_type, self, attr='declarator')

    def get_children(self) -> List[Node]:
        return [self.declarator]

    def get_children_names(self) -> List[str]:
        return ['declarator']

    def to_string(self) -> str:
        return self.declarator.to_string()


class TypedFormalParameter(FormalParameter):

    def __init__(self, node_type: NodeType, decl: Declarator, decl_type: DeclaratorType):
        super().__init__(node_type)
        self.declarator = decl
        self.decl_type = decl_type
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.FORMAL_PARAMETER:
            throw_invalid_type(self.node_type, self)
        if self.decl_type.node_type != NodeType.DECLARATOR_TYPE:
            throw_invalid_type(self.decl_type.node_type, self, attr='decl_type')
        if not is_declarator(self.declarator):
            throw_invalid_type(self.declarator, self, attr='declarator')

    def get_children(self) -> List[Node]:
        return [self.decl_type, self.declarator]

    def get_children_names(self) -> List[str]:
        return ['decl_type', 'declarator']

    def to_string(self) -> str:
        return f'{self.decl_type.to_string()} {self.declarator.to_string()}'


class SpreadParameter(FormalParameter):

    def __init__(self, node_type: NodeType, decl: Declarator, decl_type: DeclaratorType):
        super().__init__(node_type)
        self.declarator = decl
        self.decl_type = decl_type
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.SPREAD_PARAMETER:
            throw_invalid_type(self.node_type, self)
        if self.decl_type.node_type != NodeType.DECLARATOR_TYPE:
            throw_invalid_type(self.decl_type.node_type, self, attr='decl_type')
        if not is_declarator(self.declarator):
            throw_invalid_type(self.declarator, self, attr='declarator')

    def get_children(self) -> List[Node]:
        return [self.decl_type, self.declarator]

    def get_children_names(self) -> List[str]:
        return ['decl_type', 'declarator']

    def to_string(self) -> str:
        return f'{self.decl_type.to_string()} ...{self.declarator.to_string()}'


class FormalParameterList(NodeList):
    node_list: List[FormalParameter]

    def __init__(
        self,
        node_type: NodeType,
        parameters: List[FormalParameter],
    ):
        super().__init__(node_type)
        self.node_list = parameters
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.FORMAL_PARAMETER_LIST:
            throw_invalid_type(self.node_type, self)
        for i, param in enumerate(self.node_list):
            if not is_formal_parameter(param):
                throw_invalid_type(param.node_type, self, attr=f'param#{i}')


class FunctionDeclarator(Node):

    def __init__(self,
                 node_type: NodeType,
                 return_type: TypeIdentifier,
                 name: Identifier,
                 parameters: FormalParameterList,
                 dimensions: Optional[Dimensions] = None,
                 throws: Optional[TypeIdentifierList] = None,
                 modifiers: Optional[ModifierList] = None,
                 type_params: Optional[TypeParameterList] = None):
        super().__init__(node_type)
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.dimensions = dimensions
        self.throws = throws
        self.modifiers = modifiers
        self.type_params = type_params
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
        if (self.dimensions is not None and
                self.dimensions.node_type != NodeType.DIMENSIONS):
            throw_invalid_type(self.dimensions.node_type, self, attr='dimensions')
        if (self.throws is not None and
                self.throws.node_type != NodeType.TYPE_IDENTIFIER_LIST):
            throw_invalid_type(self.throws.node_type, self, attr='throws')
        if (self.modifiers is not None and
                self.modifiers.node_type != NodeType.MODIFIER_LIST):
            throw_invalid_type(self.modifiers.node_type, self, attr='modifiers')
        if (self.type_params is not None and
                self.type_params.node_type != NodeType.TYPE_PARAMETER_LIST):
            throw_invalid_type(self.type_params.node_type, self, attr='type_params')

    def to_string(self) -> str:
        ret_type_str = self.return_type.to_string()
        name_str = self.name.to_string()
        params_str = ', '.join(
            param.to_string() for param in self.parameters.get_children())
        res = f'{ret_type_str} {name_str}({params_str})'

        if self.type_params is not None:
            type_param_str = self.type_params.to_string()
            res = f'{type_param_str} {res}'

        if self.modifiers is not None:
            modifiers_str = ' '.join(
                modifier.to_string() for modifier in self.modifiers.get_children())
            res = f'{modifiers_str} {res}'

        if self.throws is not None:
            throws_str = ', '.join(
                throw.to_string() for throw in self.throws.get_children())
            res = f'{res} throws {throws_str}'

        return res

    def get_children(self) -> List[Node]:
        children = []
        if self.modifiers is not None:
            children.append(self.modifiers)
        if self.type_params is not None:
            children.append(self.type_params)
        children.append(self.return_type)
        children.append(self.name)
        children.append(self.parameters)
        if self.dimensions is not None:
            children.append(self.dimensions)
        if self.throws is not None:
            children.append(self.throws)

        return children

    def get_children_names(self) -> List[str]:
        return [
            'modifiers', 'type_parameters', 'return_type', 'name', 'parameters',
            'dimensions', 'throws'
        ]


class FunctionDeclaration(Statement):

    def __init__(self, node_type: NodeType, declarator: FunctionDeclarator,
                 body: Union[BlockStatement, EmptyStatement]):
        super().__init__(node_type)
        self.declarator = declarator
        self.body = body
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.FUNC_DECLARATION:
            throw_invalid_type(self.node_type, self)
        if self.declarator.node_type != NodeType.FUNC_DECLARATOR:
            throw_invalid_type(self.declarator.node_type, self, attr='decorator')
        if (self.body.node_type != NodeType.BLOCK_STMT and
                self.body.node_type != NodeType.EMPTY_STMT):
            throw_invalid_type(self.body.node_type, self, attr='body')

    def to_string(self) -> str:
        return f'{self.declarator.to_string()} {self.body.to_string()}'

    def get_children(self) -> List[Node]:
        return [self.declarator, self.body]

    def get_children_names(self) -> List[str]:
        return ['declarator', 'body']
