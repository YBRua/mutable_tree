import unittest
from .transform_test_base import TransformTestBase
from tree_manip.transforms import ForToWhileVisitor, WhileToForVisitor


class TestLoopTransform(TransformTestBase):

    def test_for_to_while(self):
        visitor = ForToWhileVisitor()
        code = 'for (int i = 0; i < 10; ++i) { print(i); }'
        self.check_transform(code, visitor)

        code = ('for (int i = 0; i < 10; ++i) '
                'for (int j = 0; j < 10; ++j) { print(i); print(j); }')
        self.check_transform(code, visitor)

        code = 'for (; i < 10; ++i) { print(i); }'
        self.check_transform(code, visitor)

        code = 'for (i = 0;; ++i) { print(i); }'
        self.check_transform(code, visitor)

        code = 'for (int i = 0; i < 10;) { print(i); }'
        self.check_transform(code, visitor)

        code = 'for (int i = 0; i < 10; ++i);'
        self.check_transform(code, visitor)

        code = 'for (int i = 0; i < 10;);'
        self.check_transform(code, visitor)

    def test_while_to_for(self):
        visitor = WhileToForVisitor()
        code = 'while (foo.bar()) { print(foo.getFoo()); }'
        self.check_transform(code, visitor)

        code = 'while (true);'
        self.check_transform(code, visitor)


if __name__ == '__main__':
    unittest.main()
