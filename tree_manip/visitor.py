from mutable_tree.nodes import Node
from typing import Optional


class Visitor:

    def generic_visit(self,
                      node: Node,
                      parent: Optional[Node] = None,
                      parent_attr: Optional[str] = None):
        print(f'generic_visit: {type(node).__name__}')
        print(node.get_children_names())
        for child_attr in node.get_children_names():
            child = node.get_child_at(child_attr)
            print(child)
            if child is not None:
                self.visit(child, node, child_attr)

    def visit(self,
              node: Node,
              parent: Optional[Node] = None,
              parent_attr: Optional[str] = None):
        print(f'visiting {type(node).__name__}')
        visitor = getattr(self, f'visit_{type(node).__name__}', self.generic_visit)
        visitor(node, parent, parent_attr)

        return node
