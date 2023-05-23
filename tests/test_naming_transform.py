import unittest
from .transform_test_base import TransformTestBase
from mutable_tree.tree_manip.transforms import ToCamelCaseVisitor, ToPascalCaseVisitor, ToSnakeCaseVisitor, ToUnderscoreCaseVisitor


class TestNamingTransform(TransformTestBase):

    def test_to_camel_case(self):
        visitor = ToCamelCaseVisitor()
        verbose = True

        code = '''
        int camelCase, PascalCase; 
        int snake_case = 1; 
        for(int _underscore_init = 1; ;) {
          camelCase = _underscore_init + snake_case;
        }
        Error IOError;
        int iOSVersion;
        '''
        self.check_transform(code, visitor, verbose=verbose)

    def test_to_pascal_case(self):
        visitor = ToPascalCaseVisitor()
        verbose = True

        code = '''
        int camelCase, PascalCase; 
        int snake_case = 1; 
        for(int _underscore_init = 1; ;) {
          camelCase = _underscore_init + snake_case;
        }
        Error IOError;
        int iOSVersion;
        '''
        self.check_transform(code, visitor, verbose=verbose)

    def test_to_snake_case(self):
        visitor = ToSnakeCaseVisitor()
        verbose = True

        code = '''
        int camelCase, PascalCase; 
        int snake_case = 1; 
        for(int _underscore_init = 1; ;) {
          camelCase = _underscore_init + snake_case;
        }
        Error IOError;
        int iOSVersion;
        '''
        self.check_transform(code, visitor, verbose=verbose)

    def test_to_underscore_case(self):
        visitor = ToUnderscoreCaseVisitor()
        verbose = True

        code = '''
        int camelCase, PascalCase; 
        int snake_case = 1; 
        for(int _underscore_init = 1; ;) {
          camelCase = _underscore_init + snake_case;
        }
        Error IOError;
        int iOSVersion;
        '''
        self.check_transform(code, visitor, verbose=verbose)


if __name__ == '__main__':
    unittest.main()
