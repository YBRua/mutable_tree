import unittest
from .js_test_base import JavaScriptSnippetTestBase


class TestJavaScriptArrayAccess(JavaScriptSnippetTestBase):

    def test_array_access(self):
        self._stmt_round_trip('arr[1];')
        self._stmt_round_trip('arr[a];')

    def test_ndarray_access(self):
        self._stmt_round_trip('array2d[a][23];')
        self._stmt_round_trip('array2d[1][23];')
        self._stmt_round_trip('array2d[1][a];')
        self._stmt_round_trip('array2d[a][b][c];')

    def test_nested_array_access(self):
        self._stmt_round_trip('a1[a2[1][2]];')
        self._stmt_round_trip('a1[a2[1]][a3[i2]];')
        self._stmt_round_trip('a1[a2[i1]][a3[1]];')

    def test_optional_array_access(self):
        self._stmt_round_trip('arr?.[1];')
        self._stmt_round_trip('arr?.[a]?.[b];')


class TestJavaScriptAssignmentExpr(JavaScriptSnippetTestBase):

    def test_assignment_expr(self):
        self._stmt_round_trip('a = 1;')
        self._stmt_round_trip('a = b;')
        self._stmt_round_trip('a = b = c;')

    def test_assignop_expr(self):
        operators = [
            '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '>>>=', '**=',
            '??=', '||=', '&&='
        ]
        for op in operators:
            self._stmt_round_trip(f'a {op} b;')
            self._stmt_round_trip(f'a {op} b {op} c;')


class TestJavaScriptBinaryExpr(JavaScriptSnippetTestBase):

    def test_binary_expr(self):
        operators = ['+', '-', '*', '/', '%', '&', '|', '^', '<<', '>>', '>>>']
        for op in operators:
            self._stmt_round_trip(f'a {op} b;')
            self._stmt_round_trip(f'a {op} 2 {op} c;')

        for op1 in operators:
            for op2 in operators:
                self._stmt_round_trip(f'a {op1} b {op2} c;')

        operators = ['&&', '||']
        for op in operators:
            self._stmt_round_trip(f'a {op} true;')
            self._stmt_round_trip(f'a {op} false {op} c;')

        operators = ['===', '!==', '**', '??', 'instanceof', 'in']
        for op in operators:
            self._stmt_round_trip(f'a {op} b;')

    def test_binary_with_assignment(self):
        operators = ['+', '-', '*', '/', '%', '&', '|', '^', '<<', '>>', '>>>', '??']
        for op in operators:
            self._stmt_round_trip(f'a = a {op} b;')


class TestJavaScriptFieldAccess(JavaScriptSnippetTestBase):

    def test_field_access(self):
        self._stmt_round_trip('foo.bar;')
        self._stmt_round_trip('foo.bar.baz;')

    def test_field_access_with_assignment(self):
        self._stmt_round_trip('foo.bar = 42;')
        self._stmt_round_trip('foo.bar.baz = 42;')
        self._stmt_round_trip('foo.bar = foo.bar + 42;')

    def test_mixed_access(self):
        self._stmt_round_trip('foo.bar.baz[1];')
        self._stmt_round_trip('foo.bar.baz[1].thonk;')
        self._stmt_round_trip('foo.bar.baz[idx].thonk[2];')

    def test_optional_field_access(self):
        self._stmt_round_trip('foo?.bar;')
        self._stmt_round_trip('foo?.bar?.baz;')
        self._stmt_round_trip('foo?.bar[1]?.[baz]?.yoo;')


class TestJavaScriptCallExpr(JavaScriptSnippetTestBase):

    def test_simple_call(self):
        self._stmt_round_trip('foo();')
        self._stmt_round_trip('foo(a);')
        self._stmt_round_trip('foo(a, b + 42);')

    def test_method_invocation(self):
        self._stmt_round_trip('foo.bar();')
        self._stmt_round_trip('boo.foo.bar(a);')
        self._stmt_round_trip('boo.foo.bar(a.thonk(), b + 42);')

    def test_mixed_invocation(self):
        self._stmt_round_trip('foo.bar().baz;')
        self._stmt_round_trip('foo.bar().baz[1] + boo.far().gaz();')

    def test_optional_invocation(self):
        self._stmt_round_trip('foo?.bar?.();')
        self._stmt_round_trip('foo?.bar?.(a)?.[b]?.();')


class TestJavaScriptNewExpr(JavaScriptSnippetTestBase):

    def test_simple_new(self):
        self._stmt_round_trip('new Foo();')
        self._stmt_round_trip('new Foo(a);')
        self._stmt_round_trip('new Foo(a, b + 42);')

    def test_complicated_new(self):
        self._stmt_round_trip('new Foo().bar;')
        self._stmt_round_trip('new Foo(new Bar(), b + 42);')

    def test_constructor(self):
        self._stmt_round_trip('new foo.Bar();')
        self._stmt_round_trip('new foo.Bar(a, b);')


class TestJavaScriptArrayCreationExpr(JavaScriptSnippetTestBase):

    def test_array_expr(self):
        self._stmt_round_trip('[1, 2, 3];')
        self._stmt_round_trip('b = [a, b, [c, d]];')
        self._stmt_round_trip('[...a, ...b];')


class TestJavaScriptTernaryExpr(JavaScriptSnippetTestBase):

    def test_simple_ternary(self):
        self._stmt_round_trip('a ? b : c;')
        self._stmt_round_trip('isTrue == true ? true : false;')

    def test_nested_ternary(self):
        self._stmt_round_trip('a ? b ? c : d : e;')
        self._stmt_round_trip('a ? b : c ? d : e;')
        self._stmt_round_trip('a ? b ? c : d : e ? f : g;')

    def test_ternary_with_exprs(self):
        self._stmt_round_trip('a ? b + 42 : c - 42;')
        self._stmt_round_trip('a ? b + 42 : c - 42 ? d + 42 : e - 42;')


class TestJavaScriptThisExpr(JavaScriptSnippetTestBase):

    def test_this_expr(self):
        self._stmt_round_trip('this;')
        self._stmt_round_trip('this.foo;')
        self._stmt_round_trip('this.foo.bar;')


class TestJavaScriptUnaryExpr(JavaScriptSnippetTestBase):

    def test_unary_expr(self):
        for op in ['+', '-', '~', '!', 'typeof', 'void', 'delete']:
            self._stmt_round_trip(f'{op}a;')
            self._stmt_round_trip(f'{op}a.b;')
            self._stmt_round_trip(f'c + {op}a;')


class TestJavaScriptParenthesizedExpr(JavaScriptSnippetTestBase):

    def test_parenthesized_expr(self):
        self._stmt_round_trip('(a);')
        self._stmt_round_trip('(a + b) * c;')
        self._stmt_round_trip('a + (b * c);')

    def test_nested_parenthesized_expr(self):
        self._stmt_round_trip('((a));')
        self._stmt_round_trip('((a + b) * c) / 10;')
        self._stmt_round_trip('(a + (b * c)) / 10;')
        self._stmt_round_trip('((a + b) * (c + d)) / (m + (m * n));')

    def test_parenthesized_call(self):
        self._stmt_round_trip('(a + b).bar();')


class TestJavaScriptYieldExpr(JavaScriptSnippetTestBase):

    def test_yield(self):
        self._stmt_round_trip('yield;')

    def test_yield_with_param(self):
        self._stmt_round_trip('yield a;')
        self._stmt_round_trip('yield a + 42;')

    def test_yield_delegate(self):
        self._stmt_round_trip('yield* a;')
        self._stmt_round_trip('yield* a + 42;')


class TestJavaScriptAwaitExpr(JavaScriptSnippetTestBase):

    def test_await(self):
        self._stmt_round_trip('await a;')
        self._stmt_round_trip('await a + 42;')
        self._stmt_round_trip('await thingy();')


class TestJavaScriptSequenceExpr(JavaScriptSnippetTestBase):
    def test_sequence_expr(self):
        self._stmt_round_trip('a, b;')
        self._stmt_round_trip('(a = 1, b = 2), c = 3;')
        self._stmt_round_trip('a = b, c, d();')


# class TestJavaLambdaExpr(JavaScriptSnippetTestBase):

#     def test_identifier_lambda(self):
#         self._stmt_round_trip('a -> a + 42;')
#         self._stmt_round_trip('a -> { int b = a + 42; return b; };')

#     def test_typed_lambda(self):
#         self._stmt_round_trip('(int a) -> a + 42;')
#         self._stmt_round_trip('(int a, int b) -> { int c = a + b; return c; };')

#     def test_inferred_lambda(self):
#         self._stmt_round_trip('(a) -> a + 42;')
#         self._stmt_round_trip('(a, b) -> { int c = a + b; return c; };')

if __name__ == '__main__':
    unittest.main()
