import unittest
from .transform_test_base import TransformTestBase
from mutable_tree.tree_manip.visitors import (
    ToCamelCaseVisitor,
    ToPascalCaseVisitor,
    ToSnakeCaseVisitor,
    ToUnderscoreCaseVisitor,
)


class TestNamingTransform(TransformTestBase):
    def test_to_camel_case(self):
        visitor = ToCamelCaseVisitor()
        verbose = False

        code = """
        int camelCase, PascalCase; 
        int snake_case = 1; 
        for(int _underscore_init = 1; ;) {
          camelCase = _underscore_init + snake_case;
        }
        Error IOError;
        int iOSVersion;
        """
        self.check_transform(code, visitor, verbose=verbose)

    def test_to_pascal_case(self):
        visitor = ToPascalCaseVisitor()
        verbose = False

        code = """
        int camelCase, PascalCase; 
        int snake_case = 1; 
        for(int _underscore_init = 1; ;) {
          camelCase = _underscore_init + snake_case;
        }
        Error IOError;
        int iOSVersion;
        """
        self.check_transform(code, visitor, verbose=verbose)

    def test_to_snake_case(self):
        visitor = ToSnakeCaseVisitor()
        verbose = False

        code = """
        int camelCase, PascalCase; 
        int snake_case = 1; 
        for(int _underscore_init = 1; ;) {
          camelCase = _underscore_init + snake_case;
        }
        Error IOError;
        int iOSVersion;
        """
        self.check_transform(code, visitor, verbose=verbose)

    def test_to_underscore_case(self):
        visitor = ToUnderscoreCaseVisitor()
        verbose = False

        code = """
        int camelCase, PascalCase; 
        int snake_case = 1; 
        for(int _underscore_init = 1; ;) {
          camelCase = _underscore_init + snake_case;
        }
        Error IOError;
        int iOSVersion;
        """
        self.check_transform(code, visitor, verbose=verbose)


if __name__ == "__main__":
    unittest.main()
