from mutable_tree.nodes import Node, NodeList
from mutable_tree.nodes import is_statement
from mutable_tree.nodes import node_factory
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
                should_update, new_nodes = self._visit(child, node, child_attr)
                if should_update:
                    self._node_update(node, child_attr, new_nodes)

        return (False, [])

    def _node_update(self, node: Node, child_attr: str, new_nodes: List[Node]):
        if isinstance(node, NodeList):
            node.replace_child_at(child_attr, new_nodes)
        elif len(new_nodes) == 1:
            node.set_child_at(child_attr, new_nodes[0])
        else:
            if is_statement(node):
                stmt_list = node_factory.create_statement_list(new_nodes)
                node.set_child_at(child_attr, node_factory.create_block_stmt(stmt_list))
            else:
                raise NotImplementedError('can only insert multiple statement nodes')

    def _visit(self,
               node: Node,
               parent: Optional[Node] = None,
               parent_attr: Optional[str] = None):
        visitor = getattr(self, f'visit_{type(node).__name__}', self.generic_visit)
        return visitor(node, parent, parent_attr)

    def visit(self, node: Node):
        self._visit(node)
        return node
