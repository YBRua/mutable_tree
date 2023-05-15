from ..node import Node, NodeType
from .statement import Statement
from .statement import is_statement
from .local_var_decl import LocalVariableDeclaration
from ..expressions import Expression, ExpressionList
from ..expressions import is_expression
from ..utils import throw_invalid_type
from typing import Union, List, Optional

ForInit = Union[LocalVariableDeclaration, ExpressionList]


class ForStatement(Statement):

    def __init__(self,
                 node_type: NodeType,
                 body: Statement,
                 init: Optional[ForInit] = None,
                 condition: Optional[Expression] = None,
                 update: Optional[ExpressionList] = None):
        super().__init__(node_type)
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body
        if self.init is not None:
            self.is_init_decl = isinstance(init, LocalVariableDeclaration)
        self._check_types()

    def _check_types(self):
        if self.node_type != NodeType.FOR_STMT:
            throw_invalid_type(self.node_type, self)

        if self.init is not None:
            if self.is_init_decl and self.init.node_type != NodeType.LOCAL_VAR_DECL:
                throw_invalid_type(self.init.node_type, self, attr='init')
            if not self.is_init_decl and self.init.node_type != NodeType.EXPRESSION_LIST:
                throw_invalid_type(self.init.node_type, self, attr='init')

        if self.condition is not None:
            if not is_expression(self.condition):
                throw_invalid_type(self.condition.node_type, self, attr='condition')

        if self.update is not None:
            if self.update.node_type != NodeType.EXPRESSION_LIST:
                throw_invalid_type(self.update.node_type, self, attr='update')

        if not is_statement(self.body):
            throw_invalid_type(self.body.node_type, self, attr='body')

    def to_string(self) -> str:
        if self.init is None:
            init_str = ';'
        elif self.is_init_decl:
            init_str = self.init.to_string()
        else:
            init_str = ', '.join(init.to_string()
                                 for init in self.init.get_children()) + ';'

        if self.condition is None:
            cond_str = ';'
        else:
            cond_str = ' ' + self.condition.to_string() + ';'

        if self.update is None:
            update_str = ''
        else:
            update_str = ' ' + ', '.join(u.to_string()
                                         for u in self.update.get_children())

        body_str = self.body.to_string()
        return f'for ({init_str}{cond_str}{update_str}) {body_str}'

    def get_children(self) -> List[Node]:
        children = []
        if self.init is not None:
            children.append(self.init)
        if self.condition is not None:
            children.append(self.condition)
        if self.update is not None:
            children.append(self.update)
        children.append(self.body)
        return children

    def get_children_names(self) -> List[str]:
        return ['init', 'condition', 'update', 'body']
