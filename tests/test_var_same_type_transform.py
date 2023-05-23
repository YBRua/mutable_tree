import unittest
from .transform_test_base import TransformTestBase
from mutable_tree.tree_manip.transforms import SplitVarWithSameTypeVisitor, MergeVarWithSameTypeVisitor


class TestVarSameType(TransformTestBase):
    def test_to_split_same_type(self):
        visitor = SplitVarWithSameTypeVisitor()
        verbose = True
        #

        code = '''
        int i, c = 1, j;
        int a = 10, b = 11;
        double d = 0.0;
        int k = 0;
        for (int p = 1, q=1;;) {
          int[] arr1, arr2;
        }
        '''
        self.check_transform(code, visitor, verbose=verbose)

    def test_to_merge_same_type(self):
        visitor = MergeVarWithSameTypeVisitor()
        verbose = True

        code = '''
        int i, a = 10, b;
        int j;
        double d = 0.0;
        double d = a;
        for (int p = 1, q = 1;;) {
        int[] arr1;
        int k = 0;
        int[] arr2;
        }
        '''
        self.check_transform(code, visitor, verbose=verbose)


if __name__ == '__main__':
    unittest.main()
