import unittest
from .transform_test_base import TransformTestBase
from mutable_tree.tree_manip.visitors import SplitVarInitVisitor


class TestVarDeclToHeadTransform(TransformTestBase):
    def test_split_var_init(self):
        visitor = SplitVarInitVisitor()
        verbose = True

        code = '''
        int a, b=1, i; 
        int[] arr1, arr2= new int[2];
        for (i = 0; i < 10; i++) {}
        for (int j = 0; j < 10; j++) {}
        '''
        self.check_transform(code, visitor, verbose=verbose)


if __name__ == '__main__':
    unittest.main()
