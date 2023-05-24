from .visitor import TransformingVisitor
from mutable_tree.nodes import Node, node_factory, LocalVariableDeclaration, \
    StatementList, Declarator, InitializingDeclarator, VariableDeclarator, AssignmentOps
from typing import Optional, List
from .var_same_type import split_DeclaratorList_by_Initializing


class SplitVarInitVisitor(TransformingVisitor):
    def visit_StatementList(self,
                            node: StatementList,
                            parent: Optional[Node] = None,
                            parent_attr: Optional[str] = None):
        self.generic_visit(node, parent, parent_attr)
        new_children_list = []
        init_decl_list = []
        for child_attr in node.get_children_names():
            child = node.get_child_at(child_attr)
            if child is None:
                continue
            if isinstance(child, LocalVariableDeclaration):
                with_init_declarator_list, without_init_declarator_list = \
                    split_DeclaratorList_by_Initializing(child.declarators)

                if without_init_declarator_list is not None:
                    declarators = without_init_declarator_list.node_list
                else:
                    declarators: List[Declarator] = []

                stmts = []
                if with_init_declarator_list is not None:
                    for initializing_declarator in with_init_declarator_list.node_list:
                        if isinstance(initializing_declarator.declarator, VariableDeclarator):
                            variable_declarator, stmt = split_initializing_declarator(initializing_declarator)
                            declarators.append(variable_declarator)
                            stmts.append(stmt)
                        else:
                            # TODO 一些指针/数组的声明应该要特殊处理, 尤其是c/c++
                            pass
                if len(declarators) > 0:
                    declarator_list = node_factory.create_declarator_list(declarators)
                    new_child = node_factory.create_local_variable_declaration(child.type, declarator_list)
                    new_children_list.append(new_child)
                for stmt in stmts:
                    new_children_list.append(stmt)
            else:
                new_children_list.append(child)
        node.node_list = new_children_list
        return False, []


def split_initializing_declarator(node: InitializingDeclarator):
    assert isinstance(node.declarator, VariableDeclarator)
    identifier = node.declarator.decl_id
    variable_declarator = node_factory.create_variable_declarator(identifier)
    assignment_expression = node_factory.create_assignment_expr(
        identifier, node.value, AssignmentOps.EQUAL)
    stmt = node_factory.create_expression_stmt(assignment_expression)
    return variable_declarator, stmt
