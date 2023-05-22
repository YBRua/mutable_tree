from ..nodes import Node
from .code_transformer import CodeTransformer
from typing import List, Dict, Sequence


class TransformerPipeline:

    def __init__(self, transformers: List[CodeTransformer]) -> None:
        self.transformers: Dict[str, CodeTransformer] = {
            transformer.name: transformer
            for transformer in transformers
        }

    def mutable_tree_transform(self, node: Node, keys: Sequence[str]) -> Node:
        for key in keys:
            name = key.split('.')[0]
            node = self.transformers[name].mutable_tree_transform(node, key)
        return node
