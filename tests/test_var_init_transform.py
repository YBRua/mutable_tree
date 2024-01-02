import unittest
from .transform_test_base import TransformTestBase
from mutable_tree.tree_manip.visitors import (
    SplitVarInitAndDeclVisitor,
    MergeVarInitAndDeclVisitor,
)


class TestVarDeclToHeadTransform(TransformTestBase):
    def test_split_var_init_and_decl(self):
        visitor = SplitVarInitAndDeclVisitor()
        verbose = False

        java_code = """
        int a, b=1, i;
        for (i = 0; i < 10; i++) {
            int[] arr1, arr2= new int[2];
        }
        for (int j = 0; j < 10; j++) {}
        """
        self.check_transform(java_code, visitor, verbose=verbose)

        # c_code = '''
        # int *p = nullptr;
        # '''
        # self.check_transform(c_code, visitor, verbose=verbose)

    def test_merge_var_init_and_decl(self):
        visitor = MergeVarInitAndDeclVisitor()
        verbose = False
        code = """
        int a, i, b;
        b = 1;
        for (i = 0; i < 10; i++) {
            int[] arr1, arr2;
        arr2 = new int[2];
        }
        for (int j = 0; j < 10; j++) {

        }
        """
        self.check_transform(code, visitor, verbose=verbose)


if __name__ == "__main__":
    unittest.main()
