import unittest
from .transform_test_base import TransformTestBase
from mutable_tree.tree_manip.transforms import (PrefixUpdateVisitor, PostfixUpdateVisitor,
                                                AssignUpdateVisitor, BinopUpdateVisitor)


class TestIncrementTransform(TransformTestBase):

    def test_prefix_update(self):
        visitor = PrefixUpdateVisitor()
        verbose = False
        self.check_transform('++i;', visitor, verbose=verbose)
        self.check_transform('i++;', visitor, verbose=verbose)
        self.check_transform('--i;', visitor, verbose=verbose)
        self.check_transform('i--;', visitor, verbose=verbose)

        self.check_transform('i = i + 1;', visitor, verbose=verbose)
        self.check_transform('i = i - 1;', visitor, verbose=verbose)

        self.check_transform('i += 1;', visitor, verbose=verbose)
        self.check_transform('i -= 1;', visitor, verbose=verbose)

        self.check_transform('i = j + 1;', visitor, verbose=verbose)
        self.check_transform('i = j - 1;', visitor, verbose=verbose)
        self.check_transform('i = 1 + i;', visitor, verbose=verbose)
        self.check_transform('i = 1 - i;', visitor, verbose=verbose)
        self.check_transform('i = i + 2;', visitor, verbose=verbose)
        self.check_transform('i = i - 2;', visitor, verbose=verbose)

        self.check_transform('for (int i = 0; i < 10; i++) { print(i); }',
                             visitor,
                             verbose=verbose)
        self.check_transform('while (i < 10) { i++; }', visitor, verbose=verbose)

    def test_postfix_update(self):
        visitor = PostfixUpdateVisitor()
        verbose = False
        self.check_transform('++i;', visitor, verbose=verbose)
        self.check_transform('i++;', visitor, verbose=verbose)
        self.check_transform('--i;', visitor, verbose=verbose)
        self.check_transform('i--;', visitor, verbose=verbose)

        self.check_transform('i = i + 1;', visitor, verbose=verbose)
        self.check_transform('i = i - 1;', visitor, verbose=verbose)

        self.check_transform('i += 1;', visitor, verbose=verbose)
        self.check_transform('i -= 1;', visitor, verbose=verbose)

        self.check_transform('i = j + 1;', visitor, verbose=verbose)
        self.check_transform('i = j - 1;', visitor, verbose=verbose)
        self.check_transform('i = 1 + i;', visitor, verbose=verbose)
        self.check_transform('i = 1 - i;', visitor, verbose=verbose)
        self.check_transform('i = i + 2;', visitor, verbose=verbose)
        self.check_transform('i = i - 2;', visitor, verbose=verbose)

        self.check_transform('for (int i = 0; i < 10; i++) { print(i); }',
                             visitor,
                             verbose=verbose)
        self.check_transform('while (i < 10) { i++; }', visitor, verbose=verbose)

    def test_assign_update(self):
        visitor = AssignUpdateVisitor()
        verbose = False
        self.check_transform('++i;', visitor, verbose=verbose)
        self.check_transform('i++;', visitor, verbose=verbose)
        self.check_transform('--i;', visitor, verbose=verbose)
        self.check_transform('i--;', visitor, verbose=verbose)

        self.check_transform('i = i + 1;', visitor, verbose=verbose)
        self.check_transform('i = i - 1;', visitor, verbose=verbose)

        self.check_transform('i += 1;', visitor, verbose=verbose)
        self.check_transform('i -= 1;', visitor, verbose=verbose)

        self.check_transform('i = j + 1;', visitor, verbose=verbose)
        self.check_transform('i = j - 1;', visitor, verbose=verbose)
        self.check_transform('i = 1 + i;', visitor, verbose=verbose)
        self.check_transform('i = 1 - i;', visitor, verbose=verbose)
        self.check_transform('i = i + 2;', visitor, verbose=verbose)
        self.check_transform('i = i - 2;', visitor, verbose=verbose)

        self.check_transform('for (int i = 0; i < 10; i++) { print(i); }',
                             visitor,
                             verbose=verbose)
        self.check_transform('while (i < 10) { i++; }', visitor, verbose=verbose)

    def test_binop_update(self):
        visitor = BinopUpdateVisitor()
        verbose = False
        self.check_transform('++i;', visitor, verbose=verbose)
        self.check_transform('i++;', visitor, verbose=verbose)
        self.check_transform('--i;', visitor, verbose=verbose)
        self.check_transform('i--;', visitor, verbose=verbose)

        self.check_transform('i = i + 1;', visitor, verbose=verbose)
        self.check_transform('i = i - 1;', visitor, verbose=verbose)

        self.check_transform('i += 1;', visitor, verbose=verbose)
        self.check_transform('i -= 1;', visitor, verbose=verbose)

        self.check_transform('i = j + 1;', visitor, verbose=verbose)
        self.check_transform('i = j - 1;', visitor, verbose=verbose)
        self.check_transform('i = 1 + i;', visitor, verbose=verbose)
        self.check_transform('i = 1 - i;', visitor, verbose=verbose)
        self.check_transform('i = i + 2;', visitor, verbose=verbose)
        self.check_transform('i = i - 2;', visitor, verbose=verbose)

        self.check_transform('for (int i = 0; i < 10; i++) { print(i); }',
                             visitor,
                             verbose=verbose)
        self.check_transform('while (i < 10) { i++; }', visitor, verbose=verbose)


if __name__ == '__main__':
    unittest.main()
