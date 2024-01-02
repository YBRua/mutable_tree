import unittest
import tree_sitter
from mutable_tree.adaptors import JavaAdaptor
from mutable_tree.stringifiers import JavaStringifier
from tree_sitter import Language, Parser

from .utils import LANGUAGES_PATH, collect_tokens


class JavaSnippetTestBase(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Parser()
        self.parser.set_language(Language(LANGUAGES_PATH, "java"))
        self.stringifier = JavaStringifier()

    def _stmt_round_trip(self, code: str, verbose: bool = False):
        tree = self.parser.parse(code.encode())
        root = tree.root_node
        if root.has_error:
            raise ValueError("original code is invalid")

        mutable_root = JavaAdaptor.convert_program(root)
        new_code = self.stringifier.stringify(mutable_root)

        if verbose:
            print(new_code)

        new_tree = self.parser.parse(new_code.encode())
        new_root = new_tree.root_node
        self.assertFalse(new_root.has_error)

        tokens = collect_tokens(root)
        new_tokens = collect_tokens(new_root)
        self.assertSequenceEqual(tokens, new_tokens)


class JavaFunctionTestBase(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Parser()
        self.parser.set_language(Language(LANGUAGES_PATH, "java"))
        self.stringifier = JavaStringifier()

    def _get_function_root(self, root: tree_sitter.Node):
        assert root.type == "program"
        class_decl_node = root.children[0]
        assert class_decl_node.type == "class_declaration"
        class_body_node = class_decl_node.children[3]
        assert class_body_node.type == "class_body"
        func_root_node = class_body_node.children[1]
        assert func_root_node.type == "method_declaration"
        return func_root_node

    def _function_round_trip(self, code: str, verbose: bool = False):
        wrapped = f"public class A {{\n{code}\n}}"

        tree = self.parser.parse(wrapped.encode())
        root = tree.root_node
        if root.has_error:
            raise ValueError("original code is invalid")

        func_root_node = self._get_function_root(root)

        mutable_root = JavaAdaptor.convert_function_declaration(func_root_node)
        new_code = self.stringifier.stringify(mutable_root)
        wrapped_new = f"public class A {{\n{new_code}\n}}"

        if verbose:
            print(new_code)

        new_tree = self.parser.parse(wrapped_new.encode())
        new_root = new_tree.root_node
        self.assertFalse(new_root.has_error)

        tokens = collect_tokens(root)
        new_tokens = collect_tokens(new_root)
        self.assertSequenceEqual(tokens, new_tokens)
