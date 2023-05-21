import unittest
from .transform_test_base import TransformTestBase
from mutable_tree.tree_manip.transforms import (CompoundIfVisitor)


class TestIfTransform(TransformTestBase):

    def test_compound_if(self):
        visitor = CompoundIfVisitor()
        verbose = False

        code = """
        if (x > 0) {
            if (y > 0) {
                doSomething();
            }
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        code = """
        if (x > 0) {
            if (y > 0) {
                doSomething();
            } else {
                doAnotherThing();
            }
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        code = """
        if (x > 0 || y > 0) {
            if (z > 0) {
                doSomething();
            }
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        code = """
        if (x > 0) {
            if (y > 0) {
                if (whoWritesCodeLikeThis()) {
                    beatHim();
                }
            }
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        # should not transform in these cases
        code = """
        if (x > 0) {
            if (y > 0) {
                doSomething();
            }
        } else {
            doAnotherThing();
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        code = """
        if (x > 0) {
            if (y > 0) {
                doSomething();
            }
            doAnotherThing();
            doYetAnotherThing();
        }
        """
        self.check_transform(code, visitor, verbose=verbose)


if __name__ == '__main__':
    unittest.main()
