import treelib
import tree_sitter
from tree_sitter import Parser, Language


def pprint_tree(root: tree_sitter.Node):
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


if __name__ == '__main__':
    lang = 'javascript'

    MAX_DEPTH = -1
    LANGUAGE = Language('parser/languages.so', lang)
    parser = Parser()
    parser.set_language(LANGUAGE)

    code = """
        switch (value) {
            case 1:
                doSomething();
                break;
            case 2:
                doSomethingElse();
                break;
        }
    """

    if lang == 'java':
        code = f'public class Test {{\n{code}\n}}'

    tree = parser.parse(bytes(code, 'utf-8'))
    pprint_tree(tree.root_node)
    print(tree.root_node.has_error)
