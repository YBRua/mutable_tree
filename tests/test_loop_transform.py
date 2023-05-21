import unittest
from .transform_test_base import TransformTestBase
from mutable_tree.tree_manip.transforms import ForToWhileVisitor, WhileToForVisitor


class TestLoopTransform(TransformTestBase):

    def test_for_to_while(self):
        visitor = ForToWhileVisitor()
        verbose = False

        code = 'for (int i = 0; i < 10; ++i) { print(i); }'
        self.check_transform(code, visitor, verbose=verbose)

        code = ('for (int i = 0; i < 10; ++i) '
                'for (int j = 0; j < 10; ++j) { print(i); print(j); }')
        self.check_transform(code, visitor, verbose=verbose)

        code = 'for (; i < 10; ++i) { print(i); }'
        self.check_transform(code, visitor, verbose=verbose)

        code = 'for (i = 0;; ++i) { print(i); }'
        self.check_transform(code, visitor, verbose=verbose)

        code = 'for (int i = 0; i < 10;) { print(i); }'
        self.check_transform(code, visitor, verbose=verbose)

        code = 'for (int i = 0; i < 10; ++i);'
        self.check_transform(code, visitor, verbose=verbose)

        code = 'for (int i = 0; i < 10;);'
        self.check_transform(code, visitor, verbose=verbose)

    def test_while_to_for(self):
        visitor = WhileToForVisitor()
        verbose = False

        code = 'while (foo.bar()) { print(foo.getFoo()); }'
        self.check_transform(code, visitor, verbose=verbose)

        code = 'while (true);'
        self.check_transform(code, visitor, verbose=verbose)


if __name__ == '__main__':
    unittest.main()
