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


if __name__ == '__main__':
    unittest.main()
