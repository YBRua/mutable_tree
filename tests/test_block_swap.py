import unittest
from .transform_test_base import TransformTestBase
from mutable_tree.tree_manip.visitors import NormalBlockSwapper, NegatedBlockSwapper


class TestOperandSwap(TransformTestBase):
    def test_normal_block_swap(self):
        visitor = NormalBlockSwapper()
        verbose = False
        code = """
        if (x < 0) {
            doSomething();
        } else {
            dont();
        }
        if (x <= 0) {
            doSomething();
        } else {
            dont();
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        code = """
        if (x > 0) {
            doSomething();
        } else {
            dont();
        }
        if (x >= 0) {
            doSomething();
        } else {
            dont();
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        code = """
        if (canDoIt()) {
            doSomething();
        } else {
            dont();
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        code = """
        if (x > 0) {
            doSomething();
        } else if (x < 0) {
            doAnotherThing();
        } else {
            dont();
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        code = """
        if (x == 0) {
            doSomething();
        } else {
            dont();
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        code = """
        if (x != 0) {
            doSomething();
        } else {
            dont();
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        # should not transform this
        code = """
        if (x < 0) {
            doSomething();
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

    def test_negated_block_swap(self):
        visitor = NegatedBlockSwapper()
        verbose = False
        code = """
        if (x < 0) {
            doSomething();
        } else {
            dont();
        }
        if (x <= 0) {
            doSomething();
        } else {
            dont();
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        code = """
        if (x > 0) {
            doSomething();
        } else {
            dont();
        }
        if (x >= 0) {
            doSomething();
        } else {
            dont();
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        code = """
        if (canDoIt()) {
            doSomething();
        } else {
            dont();
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        code = """
        if (x > 0) {
            doSomething();
        } else if (x < 0) {
            doAnotherThing();
        } else {
            dont();
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        code = """
        if (x == 0) {
            doSomething();
        } else {
            dont();
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        code = """
        if (x != 0) {
            doSomething();
        } else {
            dont();
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        # should not transform this
        code = """
        if (x < 0) {
            doSomething();
        }
        """
        self.check_transform(code, visitor, verbose=verbose)


if __name__ == "__main__":
    unittest.main()
