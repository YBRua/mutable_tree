import unittest
from .js_test_base import JavaScriptFunctionTestBase


class TestJavaScriptFunctionDeclaration(JavaScriptFunctionTestBase):
    def test_simple_method(self):
        self._function_round_trip("function foo() { }")
        self._function_round_trip("function foo() { let a = 1; }")

    def test_method_with_params(self):
        self._function_round_trip("function foo(a, b) { }")

    def test_method_with_modifiers(self):
        self._function_round_trip("async function foo(a) { let aa = 1; }")


if __name__ == "__main__":
    unittest.main()
