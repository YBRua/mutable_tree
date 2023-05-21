# NOTE: treelib is required to run this demo
import treelib
import tree_sitter
from mutable_tree.nodes import Node, NodeType
from mutable_tree.adaptors import JavaAdaptor


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


def pprint_mutable_ast(root: Node):
    tree = treelib.Tree()

    def _build_treelib_tree(current: Node, parent=None):

        def _format_node(node: Node):
            if (node.node_type == NodeType.IDENTIFIER
                    or node.node_type == NodeType.LITERAL):
                node_str = f'{node.node_type.value} ({node.to_string()})'
            else:
                node_str = node.node_type.value
            return node_str

        tree_node = tree.create_node(_format_node(current), parent=parent)
        for child in current.get_children():
            _build_treelib_tree(child, tree_node.identifier)

    _build_treelib_tree(root)
    tree.show(key=lambda x: True)  # keep order of insertion


def main():
    code = """
    int a = 10, b = 11;
    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < 10; j++) {
            System.out.println("Hello World");
        }
    }
    """

    # convert code to tree-sitter AST
    parser = tree_sitter.Parser()
    parser.set_language(tree_sitter.Language('./parser/languages.so', 'java'))
    tree = parser.parse(code.encode())
    pprint_treesitter(tree.root_node)

    # convert tree-sitter AST to mutable AST
    mutable_root = JavaAdaptor.convert_program(tree.root_node)
    pprint_mutable_ast(mutable_root)


if __name__ == '__main__':
    main()
