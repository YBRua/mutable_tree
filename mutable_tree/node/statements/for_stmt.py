from ..node import NodeType
from .statement import Statement
from .local_var_decl import LocalVariableDeclaration
from ..expressions import Expression
from ..utils import is_statement, is_expression
from ..utils import throw_invalid_type
from typing import Union, List

Init = Union[LocalVariableDeclaration, List[Expression]]


class ForStatement(Statement):

    def __init__(self, node_type: NodeType, init: Init, condition: Expression,
                 update: List[Expression], body: Statement):
        super().__init__(node_type)
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body
        self._check_types()
        self.is_init_decl = isinstance(init, LocalVariableDeclaration)

    def _check_types(self):
        if self.node_type != NodeType.FOR_STMT:
            throw_invalid_type(self.node_type, self)
        if self.is_init_decl and self.init.node_type != NodeType.LOCAL_VAR_DECL:
            throw_invalid_type(self.init.node_type, self, attr='init')
        if not self.is_init_decl and not is_expression(self.init):
            throw_invalid_type(self.init.node_type, self, attr='init')
        if not is_expression(self.condition):
            throw_invalid_type(self.condition.node_type, self, attr='condition')
        for i, u in enumerate(self.update):
            if not is_expression(u):
                throw_invalid_type(u.node_type, self, attr=f'update#{i}')
        if not is_statement(self.body):
            throw_invalid_type(self.body.node_type, self, attr='body')

    def to_string(self) -> str:
        if self.is_init_decl:
            init_str = self.init.to_string()
        else:
            init_str = self.init.to_string() + ';'
        cond_str = self.condition.to_string()
        update_str = ', '.join(u.to_string() for u in self.update)
        body_str = self.body.to_string()

        return f'for ({init_str} {cond_str}; {update_str}) {body_str}'
