import unittest
from tree_sitter import Language, Parser
from mutable_tree.adaptor import JavaAdaptor
from mutable_tree.node import Node, NodeType
from .utils import LANGUAGES_PATH
from typing import Callable


class TransformTestBase(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = Parser()
        self.parser.set_language(Language(LANGUAGES_PATH, 'java'))

    def _check_ast(self, code: str):
        tree = self.parser.parse(code.encode())
        root = tree.root_node
        self.assertFalse(root.has_error)

    def _statement_to_mutable(self, code: str):
        tree = self.parser.parse(code.encode())
        root = tree.root_node
        if root.has_error:
            raise ValueError('original code is invalid')
        mutable_root = JavaAdaptor.convert_statement(root.children[0])
        return mutable_root

    def check_contains_statement(self, root: Node, node_type: NodeType, count: int):
        pass

    def check_transform(self, code: str, transform_func: Callable[[Node], Node]):
        root = self._statement_to_mutable(code)
        new_root = transform_func(root)
        new_code = new_root.to_string()
        print(new_code)
        self._check_ast(new_code)
