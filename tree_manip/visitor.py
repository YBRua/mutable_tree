from mutable_tree.nodes import Node, NodeList
from typing import Optional, List


class Visitor:

    def generic_visit(self,
                      node: Node,
                      parent: Optional[Node] = None,
                      parent_attr: Optional[str] = None):
        for child_attr in node.get_children_names():
            child = node.get_child_at(child_attr)
            if child is not None:
                self._visit(child, node, child_attr)

    def _visit(self,
               node: Node,
               parent: Optional[Node] = None,
               parent_attr: Optional[str] = None):
        visitor = getattr(self, f'visit_{type(node).__name__}', self.generic_visit)
        visitor(node, parent, parent_attr)

    def visit(self, node: Node):
        self._visit(node)


class TransformingVisitor:

    def generic_visit(self,
                      node: Node,
                      parent: Optional[Node] = None,
                      parent_attr: Optional[str] = None):
        for child_attr in node.get_children_names():
            child = node.get_child_at(child_attr)
            if child is not None:
                should_update, new_stmts = self._visit(child, node, child_attr)
                if should_update:
                    self._node_update(node, child_attr, new_stmts)

        return (False, [])

    def _node_update(self, node: Node, child_attr: str, new_stmts: List[Node]):
        if isinstance(node, NodeList):
            node.replace_children_at(child_attr, len(new_stmts), new_stmts)

    def _visit(self,
               node: Node,
               parent: Optional[Node] = None,
               parent_attr: Optional[str] = None):
        visitor = getattr(self, f'visit_{type(node).__name__}', self.generic_visit)
        return visitor(node, parent, parent_attr)

    def visit(self, node: Node):
        self._visit(node)
        return node