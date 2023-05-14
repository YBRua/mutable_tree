import unittest
from mutable_tree.adaptor import JavaAdaptor
from tree_sitter import Language, Parser

from .utils import LANGUAGES_PATH, collect_tokens


class JavaExpressionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = Parser()
        self.parser.set_language(Language(LANGUAGES_PATH, 'java'))

    def _stmt_round_trip(self, code: str):
        tree = self.parser.parse(code.encode())
        root = tree.root_node
        assert not root.has_error

        mutable_root = JavaAdaptor.convert_statement(root.children[0])
        new_code = mutable_root.to_string()

        new_tree = self.parser.parse(new_code.encode())
        new_root = new_tree.root_node
        assert not new_root.has_error

        tokens = collect_tokens(root)
        new_tokens = collect_tokens(new_root)
        self.assertSequenceEqual(tokens, new_tokens)

    def test_array_access(self):
        self._stmt_round_trip('arr[1];')


if __name__ == '__main__':
    unittest.main()
