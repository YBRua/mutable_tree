import unittest
from tree_sitter import Language, Parser

from mutable_tree.adaptors import JavaAdaptor
from mutable_tree.nodes import Node, NodeType
from mutable_tree.tree_manip.visitors import TransformingVisitor

from .utils import LANGUAGES_PATH


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
        mutable_root = JavaAdaptor.convert_program(root)
        return mutable_root

    def check_contains_statement(self, root: Node, node_type: NodeType, count: int):
        pass

    def check_transform(self,
                        code: str,
                        transform_func: TransformingVisitor,
                        verbose: bool = False) -> Node:
        root = self._statement_to_mutable(code)
        new_root = transform_func.visit(root)
        new_code = new_root.to_string()
        self._check_ast(new_code)

        if verbose:
            print('##### before #####')
            print(code)
            print('##### after #####')
            print(new_code)
            print()

        return root
