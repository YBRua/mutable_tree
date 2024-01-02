import unittest
from .java_test_base import JavaFunctionTestBase


class TestJavaMethodDeclaration(JavaFunctionTestBase):
    def test_simple_method(self):
        self._function_round_trip("void foo() { }")
        self._function_round_trip("void foo() { int a = 1; }")
        self._function_round_trip("void foo();")

    def test_method_with_params(self):
        self._function_round_trip("void foo(int a, int b) { }")
        self._function_round_trip("void foo(int a, int b);")

    def test_method_with_modifiers(self):
        self._function_round_trip("public void foo(int a) { int aa = 1; }")
        self._function_round_trip("public static void foo(int a) { int aa = 1; }")

    def test_return_types(self):
        self._function_round_trip("int foo() { return 1; }")
        self._function_round_trip("public int[] foo() { return someArray(); }")

    def test_throws(self):
        self._function_round_trip("void foo() throws Exception { gogogo(); }")
        self._function_round_trip(
            "void foo() throws Exception, IOException { gogogo(); }"
        )

    def test_type_params(self):
        self._function_round_trip("public <T> T foo() { return null; }")
        self._function_round_trip("public <T extends Number> T foo() { return null; }")

    def test_spread_params(self):
        self._function_round_trip("void foo(int[]... a) { }")


if __name__ == "__main__":
    unittest.main()
