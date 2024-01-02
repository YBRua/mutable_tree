import unittest
import tree_sitter
from mutable_tree.adaptors import CppAdaptor
from mutable_tree.stringifiers import CppStringifier
from tree_sitter import Language, Parser

from .utils import LANGUAGES_PATH, collect_tokens


class CppSnippetTestBase(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Parser()
        self.parser.set_language(Language(LANGUAGES_PATH, "cpp"))
        self.stringifier = CppStringifier()

    def _stmt_round_trip(self, code: str, verbose: bool = False):
        tree = self.parser.parse(code.encode())
        root = tree.root_node
        if root.has_error:
            raise ValueError("original code is invalid")

        mutable_root = CppAdaptor.convert_program(root)
        new_code = self.stringifier.stringify(mutable_root)

        if verbose:
            print(new_code)

        new_tree = self.parser.parse(new_code.encode())
        new_root = new_tree.root_node
        self.assertFalse(new_root.has_error)

        tokens = collect_tokens(root)
        new_tokens = collect_tokens(new_root)
        self.assertSequenceEqual(tokens, new_tokens)


class CppFunctionTestBase(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Parser()
        self.parser.set_language(Language(LANGUAGES_PATH, "cpp"))
        self.stringifier = CppStringifier()

    def _get_function_root(self, root: tree_sitter.Node):
        assert root.type == "translation_unit"
        func_root_node = root.children[0]
        assert func_root_node.type == "function_definition", func_root_node.type
        return func_root_node

    def _function_round_trip(self, code: str, verbose: bool = False):
        tree = self.parser.parse(code.encode())
        root = tree.root_node
        if root.has_error:
            raise ValueError("original code is invalid")

        func_root_node = self._get_function_root(root)

        mutable_root = CppAdaptor.convert_function_definition(func_root_node)
        new_code = self.stringifier.stringify(mutable_root)

        if verbose:
            print(new_code)

        new_tree = self.parser.parse(new_code.encode())
        new_root = new_tree.root_node
        self.assertFalse(new_root.has_error)

        tokens = collect_tokens(root)
        new_tokens = collect_tokens(new_root)
        self.assertSequenceEqual(tokens, new_tokens)
