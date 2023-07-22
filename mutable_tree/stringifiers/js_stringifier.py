from mutable_tree.nodes import (ArrayAccess, ArrayExpression, CallExpression, FieldAccess,
                                YieldStatement)
from mutable_tree.nodes import SpreadElement, AwaitExpression
from .common import BaseStringifier


class JavaScriptStringifier(BaseStringifier):

    def __init__(self, semicolon: bool = True):
        super().__init__()
        self.semicolon = semicolon

    def stringify_ArrayExpression(self, node: ArrayExpression) -> str:
        children_strs = [self.stringify(elem) for elem in node.elements.get_children()]
        return f'[{", ".join(children_strs)}]'

    def stringify_ArrayAccess(self, node: ArrayAccess) -> str:
        if node.optional:
            return f'{self.stringify(node.array)}?.[{self.stringify(node.index)}]'
        else:
            return super().stringify_ArrayAccess(node)

    def stringify_FieldAccess(self, node: FieldAccess) -> str:
        object_str = self.stringify(node.object)
        field_str = self.stringify(node.field)

        if node.optional:
            return f'{object_str}?.{field_str}'
        else:
            return f'{object_str}.{field_str}'

    def stringify_CallExpression(self, node: CallExpression) -> str:
        arg_list_strs = [self.stringify(arg) for arg in node.args.get_children()]
        arg_list = ', '.join(arg_list_strs)
        if node.optional:
            return f'{self.stringify(node.callee)}?.({arg_list})'
        else:
            return f'{self.stringify(node.callee)}({arg_list})'

    def stringify_YieldStatement(self, node: YieldStatement) -> str:
        if node.expr is None:
            return 'yield'
        elif node.is_delegate:
            return f'yield* {self.stringify(node.expr)}'
        else:
            return f'yield {self.stringify(node.expr)}'

    def stringify_SpreadElement(self, node: SpreadElement) -> str:
        expr_str = self.stringify(node.expr)
        return f'...{expr_str}'

    def stringify_AwaitExpression(self, node: AwaitExpression) -> str:
        expr_str = self.stringify(node.expr)
        return f'await {expr_str}'
