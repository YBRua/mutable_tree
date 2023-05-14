import unittest
from mutable_tree.adaptor import JavaAdaptor
from tree_sitter import Language, Parser

from .utils import LANGUAGES_PATH, collect_tokens


class JavaExprTestBase(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = Parser()
        self.parser.set_language(Language(LANGUAGES_PATH, 'java'))

    def _stmt_round_trip(self, code: str):
        tree = self.parser.parse(code.encode())
        root = tree.root_node
        self.assertFalse(root.has_error)

        mutable_root = JavaAdaptor.convert_statement(root.children[0])
        new_code = mutable_root.to_string()

        new_tree = self.parser.parse(new_code.encode())
        new_root = new_tree.root_node
        self.assertFalse(new_root.has_error)

        tokens = collect_tokens(root)
        new_tokens = collect_tokens(new_root)
        self.assertSequenceEqual(tokens, new_tokens)


class TestJavaArrayAccess(JavaExprTestBase):

    def test_array_access(self):
        self._stmt_round_trip('arr[1];')
        self._stmt_round_trip('arr[a];')

    def test_ndarray_access(self):
        self._stmt_round_trip('array2d[a][23];')
        self._stmt_round_trip('array2d[1][23];')
        self._stmt_round_trip('array2d[1][a];')
        self._stmt_round_trip('array2d[a][b][c];')

    def test_nested_array_access(self):
        self._stmt_round_trip('a1[a2[1][2]];')
        self._stmt_round_trip('a1[a2[1]][a3[i2]];')
        self._stmt_round_trip('a1[a2[i1]][a3[1]];')


class TestJavaAssignmentExpr(JavaExprTestBase):

    def test_assignment_expr(self):
        self._stmt_round_trip('a = 1;')
        self._stmt_round_trip('a = b;')
        self._stmt_round_trip('a = b = c;')


if __name__ == '__main__':
    unittest.main()
