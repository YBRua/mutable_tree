import unittest
from .cpp_test_base import CppFunctionTestBase


class TestCppFunctionDefinition(CppFunctionTestBase):

    def test_simple_function(self):
        self._function_round_trip('void foo() { }')
        self._function_round_trip('void foo() { int a = 1; }')

    def test_function_with_params(self):
        self._function_round_trip('void foo(int a, int b) { dosomething(); }')
        self._function_round_trip('void foo(int* a, int& b, int** c) { dosomething(); }')
        self._function_round_trip('void foo(const int* a, char b) { dosomething(); }')

    def test_function_with_return_types(self):
        self._function_round_trip('int foo() { return 1; }')
        self._function_round_trip('int* foo() { return nullptr; }')
        self._function_round_trip('int** foo() { return nullptr; }')
        self._function_round_trip('int& foo() { return a; }')


if __name__ == '__main__':
    unittest.main()
