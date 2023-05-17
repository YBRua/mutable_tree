import unittest
from mutable_tree.adaptors import JavaAdaptor
from tree_sitter import Language, Parser

from .utils import LANGUAGES_PATH, collect_tokens


class JavaSnippetTestBase(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = Parser()
        self.parser.set_language(Language(LANGUAGES_PATH, 'java'))

    def _stmt_round_trip(self, code: str, verbose: bool = False):
        tree = self.parser.parse(code.encode())
        root = tree.root_node
        if root.has_error:
            raise ValueError('original code is invalid')

        mutable_root = JavaAdaptor.convert_program(root)
        new_code = mutable_root.to_string()

        if verbose:
            print(new_code)

        new_tree = self.parser.parse(new_code.encode())
        new_root = new_tree.root_node
        self.assertFalse(new_root.has_error)

        tokens = collect_tokens(root)
        new_tokens = collect_tokens(new_root)
        self.assertSequenceEqual(tokens, new_tokens)
