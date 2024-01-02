import unittest
from .transform_test_base import TransformTestBase
from mutable_tree.tree_manip.visitors import TernaryToIfVisitor, SwitchToIfVisitor


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

    def test_switch_to_if(self):
        visitor = SwitchToIfVisitor()
        verbose = False
        code = """
        switch (some.thing) {
            case 1:
                doSomething();
                break;
            case 2:
                doSomethingElse();
                break;
            default:
                doNothing();
                break;
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        code = """
        switch (some.thing) {
            case 1:
            {
                doSomething();
                break;
            }
            case 2:
            {
                doSomethingElse();
                break;
            }
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        code = """
        switch (pDirection) {
            case LEFT:
            case RIGHT:
                return pY;
            case UP:
                return pY - 1;
            case DOWN:
                return pY + 1;
            default:
                throw new IllegalArgumentException();
        }
        """
        self.check_transform(code, visitor, verbose=verbose)

        # should not transform
        code = """
        switch (some.thing) {
            case 1:
                doSomething();
            case 2:
            case 3:
                doSomethingElse();
            default:
                doNothing();
                break;
        }
        """
        self.check_transform(code, visitor, verbose=verbose)


if __name__ == "__main__":
    unittest.main()
