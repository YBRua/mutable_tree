import unittest
from .java_test_base import JavaSnippetTestBase


class TestJavaArrayAccess(JavaSnippetTestBase):

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


class TestJavaAssignmentExpr(JavaSnippetTestBase):

    def test_assignment_expr(self):
        self._stmt_round_trip('a = 1;')
        self._stmt_round_trip('a = b;')
        self._stmt_round_trip('a = b = c;')

    def test_assignop_expr(self):
        operators = ['+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '>>>=']
        for op in operators:
            self._stmt_round_trip(f'a {op} b;')
            self._stmt_round_trip(f'a {op} b {op} c;')


class TestJavaBinaryExpr(JavaSnippetTestBase):

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

    def test_binary_with_assignment(self):
        operators = ['+', '-', '*', '/', '%', '&', '|', '^', '<<', '>>', '>>>']
        for op in operators:
            self._stmt_round_trip(f'a = a {op} b;')


class TestJavaFieldAccess(JavaSnippetTestBase):

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


class TestJavaCallExpr(JavaSnippetTestBase):

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


if __name__ == '__main__':
    unittest.main()
