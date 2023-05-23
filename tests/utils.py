import tree_sitter
from typing import List
from os import path

LANGUAGES_PATH = None
if path.isfile('./parser/languages.so'):
    LANGUAGES_PATH = './parser/languages.so'
else:
    LANGUAGES_PATH = '/home/liwei/Code-Watermark/variable-watermark/resources/my-languages.so'


def collect_tokens(root: tree_sitter.Node) -> List[str]:
    tokens: List[str] = []

    def _collect_tokens(node: tree_sitter.Node):
        if node.child_count == 0:
            tokens.append(node.text.decode())

        for ch in node.children:
            _collect_tokens(ch)

    _collect_tokens(root)
    return tokens
