import unittest
from .transform_test_base import TransformTestBase
from mutable_tree.tree_manip.visitors import (
    MoveVarDeclToHeadVisitor,
    MoveVarDeclToBeforeUsedVisitor,
)


class TestVarDeclToHeadTransform(TransformTestBase):
    def test_var_decl_to_head(self):
        visitor = MoveVarDeclToHeadVisitor()
        verbose = False

        code = """
        doSomething();
        int a, b=1, i; 
        doSomething();
        a = 1;
        if (a > 0) {
           a = -1;
           int nestBlockDecl;
        }
        int c;
        for (i = 0; i < 10; i++) {}
        c = b + a;
        """
        self.check_transform(code, visitor, verbose=verbose)

    def test_var_decl_to_before_use(self):
        visitor = MoveVarDeclToBeforeUsedVisitor()
        verbose = False

        code = """
        int a, b = 1, i;
        doSomething();
        int c;
        if (True) {
        int nestBlockDecl;
        a = -1;
        nestBlockDecl = a;
        }
        for (i = 0; i < 10; i++) {}
        c = b + a;
        """
        self.check_transform(code, visitor, verbose=verbose)


if __name__ == "__main__":
    unittest.main()
