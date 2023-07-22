# NOTE: treelib is required to run this demo, you will have to MANUALLY install it
import treelib
import tree_sitter
from mutable_tree.nodes import Node, NodeType
from mutable_tree.adaptors import JavaAdaptor, CppAdaptor
from mutable_tree.stringifiers import BaseStringifier, CppStringifier, JavaStringifier


def pprint_treesitter(root: tree_sitter.Node):
    tree = treelib.Tree()

    def _build_treelib_tree(current: tree_sitter.Node, parent=None):

        def _format_node(node: tree_sitter.Node):
            node_text = node.text.decode()
            if node.child_count == 0:
                node_str = f'{node.type} ({node_text})'
            else:
                node_str = f'{node.type}'
            # if node.type == 'identifier':
            #     node_str = f'{node_str} ({str(node.text, "utf-8")})'
            return node_str

        tree.create_node(_format_node(current), current.id, parent=parent)
        for child in current.children:
            _build_treelib_tree(child, current.id)

    _build_treelib_tree(root)
    tree.show(key=lambda x: True)  # keep order of insertion


def pprint_mutable_ast(root: Node, stringifier: BaseStringifier):
    tree = treelib.Tree()

    def _build_treelib_tree(current: Node, parent=None):

        def _format_node(node: Node):
            if (node.node_type == NodeType.IDENTIFIER
                    or node.node_type == NodeType.LITERAL):
                node_str = f'{node.node_type.value} ({stringifier.stringify(node)})'
            else:
                node_str = node.node_type.value
            return node_str

        tree_node = tree.create_node(_format_node(current), parent=parent)
        for child in current.get_children():
            _build_treelib_tree(child, tree_node.identifier)

    _build_treelib_tree(root)
    tree.show(key=lambda x: True)  # keep order of insertion


def main():
    # java / cpp
    LANGUAGE = 'java'
    code = """
    int[] a = {1, 2, 3 ,4}
    """

    # convert code to tree-sitter AST
    parser = tree_sitter.Parser()
    LANGUAGES_PATH = './parser/languages.so'
    parser.set_language(tree_sitter.Language(LANGUAGES_PATH, LANGUAGE))

    tree = parser.parse(code.encode())
    pprint_treesitter(tree.root_node)

    # convert tree-sitter AST to mutable AST
    if LANGUAGE == 'java':
        mutable_root = JavaAdaptor.convert_program(tree.root_node)
    elif LANGUAGE == 'cpp':
        mutable_root = CppAdaptor.convert_program(tree.root_node)
    else:
        raise ValueError('only support java and cpp')
    pprint_mutable_ast(mutable_root)


if __name__ == '__main__':
    main()
