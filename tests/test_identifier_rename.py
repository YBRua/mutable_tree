import unittest
from .transform_test_base import TransformTestBase
from mutable_tree.tree_manip.visitors import IdentifierRenamingVisitor


class TestIdentifierRename(TransformTestBase):

    def test_identifier_rename(self):
        verbose = False

        code = '''
        int something = 1;
        int another_thing = 2;
        MyClass yetAnotherThing = new MyClass();
        MyClass _internal_thing = new MyClass();

        int a = something + another_thing + yetAnotherThing.value;
        int b = _internal_thing.value + 10;
        '''
        visitor = IdentifierRenamingVisitor(src_var='something', dst_var='somethingElse')
        self.check_transform(code, visitor, verbose=verbose)

        visitor = IdentifierRenamingVisitor(src_var='another_thing', dst_var='newThing')
        self.check_transform(code, visitor, verbose=verbose)

        visitor = IdentifierRenamingVisitor(src_var='yetAnotherThing', dst_var='yetYet')
        self.check_transform(code, visitor, verbose=verbose)

        visitor = IdentifierRenamingVisitor(src_var='_internal_thing',
                                            dst_var='ExternalThing')
        self.check_transform(code, visitor, verbose=verbose)


if __name__ == '__main__':
    unittest.main()
