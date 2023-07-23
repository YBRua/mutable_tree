from mutable_tree.nodes import (ArrayAccess, ArrayExpression, BreakStatement,
                                CallExpression, CatchClause, ContinueStatement,
                                DoStatement, ExpressionStatement, FieldAccess,
                                FunctionDeclaration, FunctionHeader, ReturnStatement,
                                ThrowStatement, YieldStatement)
from mutable_tree.nodes import (SpreadElement, AwaitExpression, WithStatement,
                                AnonymousDeclarator)
from .common import BaseStringifier


class JavaScriptStringifier(BaseStringifier):

    def __init__(self, semicolon: bool = True):
        super().__init__()
        self.semicolon = semicolon

    def _semicolon(self, input_str: str) -> str:
        if self.semicolon:
            return f'{input_str};'
        else:
            return input_str

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

    def stringify_ExpressionStatement(self, node: ExpressionStatement) -> str:
        expr_str = self.stringify(node.expr)
        return self._semicolon(expr_str)

    def stringify_DoStatement(self, node: DoStatement) -> str:
        do_str = (f'do\n{self.stringify(node.body)}\n'
                  f'while ({self.stringify(node.condition)})')
        return self._semicolon(do_str)

    def stringify_BreakStatement(self, node: BreakStatement) -> str:
        if node.label is not None:
            break_str = f'break {self.stringify(node.label)}'
        else:
            break_str = 'break'
        return self._semicolon(break_str)

    def stringify_ContinueStatement(self, node: ContinueStatement) -> str:
        if node.label is not None:
            continue_str = f'continue {self.stringify(node.label)}'
        else:
            continue_str = 'continue'
        return self._semicolon(continue_str)

    def stringify_ReturnStatement(self, node: ReturnStatement) -> str:
        if node.expr is None:
            return_str = 'return'
        else:
            return_str = f'return {self.stringify(node.expr)}'
        return self._semicolon(return_str)

    def stringify_ThrowStatement(self, node: ThrowStatement) -> str:
        return self._semicolon(f'throw {self.stringify(node.expr)}')

    def stringify_CatchClause(self, node: CatchClause) -> str:
        body_str = self.stringify(node.body)
        if node.exception is not None:
            parameter_str = f'({self.stringify(node.exception)})'
            return f'catch {parameter_str} {body_str}'
        else:
            return f'catch {body_str}'

    def stringify_WithStatement(self, node: WithStatement) -> str:
        obj_str = self.stringify(node.object)
        body_str = self.stringify(node.body)
        return f'with ({obj_str}) {body_str}'

    def stringify_AnonymousDeclarator(self, node: AnonymousDeclarator) -> str:
        return ''

    def stringify_FunctionHeader(self, node: FunctionHeader) -> str:
        decl_str = self.stringify(node.func_decl)

        if node.modifiers is not None:
            modifier_str = self.stringify(node.modifiers)
            return f'{modifier_str} function {decl_str}'
        else:
            return f'function {decl_str}'
