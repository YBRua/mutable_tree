import unittest
from .java_test_base import JavaSnippetTestBase


class TestJavaVarDecl(JavaSnippetTestBase):

    def test_simple_variable_decl(self):
        self._stmt_round_trip('int a;')
        self._stmt_round_trip('int a = 1;')
        self._stmt_round_trip('float a = b;')
        self._stmt_round_trip('float a = b + 1;')

    def test_multiple_decl(self):
        self._stmt_round_trip('int a, b;')
        self._stmt_round_trip('int a, b = 1;')
        self._stmt_round_trip('float a, b = c;')
        self._stmt_round_trip('float a = 1.0, b = 2.32;')

    def test_array_decl(self):
        self._stmt_round_trip('int[] a;')
        self._stmt_round_trip('int a, b[];')
        self._stmt_round_trip('float[][] a, b;')
        self._stmt_round_trip('float[][] a, b[];')
        # TODO: add initializer tests

    def test_custom_types(self):
        self._stmt_round_trip('MyClass a;')
        self._stmt_round_trip('MyClass a = myClassFactory.getNewInstance();')
        self._stmt_round_trip('MyClass a, b, c[];')


class TestJavaForStmt(JavaSnippetTestBase):

    def test_simple_for(self):
        self._stmt_round_trip('for (int i = 0; i < 10; i++) { }')
        self._stmt_round_trip('for (int i = 0; i < 10; i++);')
        self._stmt_round_trip('for (i = 0; i <= 5; i++) { }')
        self._stmt_round_trip('for (i = 0; i <= 5; i++);')

    def test_empty_for(self):
        self._stmt_round_trip('for (;;) { }')
        self._stmt_round_trip('for (;;) ;')
        self._stmt_round_trip('for (i = 1;;) { }')
        self._stmt_round_trip('for (; i < 10;) { }')
        self._stmt_round_trip('for (;; i++) { }')
    
    def test_multi_init(self):
        self._stmt_round_trip('for (int i = 0, j = 0; i < 10; i++) { }')
        self._stmt_round_trip('for (i = 0, j = 0; i < 10; i++);')
    
    def test_multi_update(self):
        self._stmt_round_trip('for (int i = 0; i < 10; i++, j++) { }')
        self._stmt_round_trip('for (i = 0; i < 10; i++, j++);')


if __name__ == '__main__':
    unittest.main()
