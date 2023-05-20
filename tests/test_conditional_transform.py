import unittest
from .transform_test_base import TransformTestBase
from mutable_tree.tree_manip.transforms import (TernaryToIfVisitor)


class TestConditionalTransform(TransformTestBase):

    def test_ternary_to_if(self):
        visitor = TernaryToIfVisitor()
        verbose = False
        code = """
        int i = x > 0 ? 1 : 0;
        int j;
        j = x > 0 ? 1 : 0;
        """
        self.check_transform(code, visitor, verbose=verbose)

        code = """
        i = canDoIt() ? x > 0 ? 1 : 0 : -1;
        """
        self.check_transform(code, visitor, verbose=verbose)

        code = """
        for (int i = 0; i < 10; i++) {
            some.thing = x > 0 ? positive() : notPositive();
        }
        """
        self.check_transform(code, visitor, verbose=verbose)


if __name__ == '__main__':
    unittest.main()
