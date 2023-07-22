from .keywords import ALL_KEYWORDS_SET
from .visitor import TransformingVisitor
from .var_name_utils import (is_underscore_case, sanitize_name_for_styling,
                             remove_preceding_underscores)
from mutable_tree.nodes import Node, node_factory, VariableDeclarator, Identifier
from typing import Optional
import inflection


class VarNamingVisitor(TransformingVisitor):
    def __init__(self):
        self.variable_name_mapping = {}

    def visit_FunctionDeclaration(self, node, parent=None, parent_attr=None):
        return (False, [])

    def visit_Identifier(self,
                         node: Identifier,
                         parent: Optional[Node] = None,
                         parent_attr: Optional[str] = None):
        name = node.name
        new_name = self.variable_name_mapping.get(name, None)

        if new_name is not None:
            decl_id = node_factory.create_identifier(new_name)
            return True, [decl_id]
        else:
            return False, []


class ToCamelCaseVisitor(VarNamingVisitor):
    def visit_VariableDeclarator(self,
                                 node: VariableDeclarator,
                                 parent: Optional[Node] = None,
                                 parent_attr: Optional[str] = None):
        name = node.decl_id.name
        if is_underscore_case(name):
            new_name = inflection.camelize(remove_preceding_underscores(name),
                                           uppercase_first_letter=False)
            new_name = sanitize_name_for_styling(new_name)
        elif all([c.isupper() for c in name]):
            # do not change if all upper case
            new_name = sanitize_name_for_styling(name)
        else:
            new_name = inflection.camelize(name, uppercase_first_letter=False)
            new_name = sanitize_name_for_styling(new_name)

        self.variable_name_mapping[name] = new_name

        decl_id = node_factory.create_identifier(new_name)
        variable_declarator = node_factory.create_variable_declarator(decl_id)
        return True, [variable_declarator]


class ToPascalCaseVisitor(VarNamingVisitor):
    def visit_VariableDeclarator(self,
                                 node: VariableDeclarator,
                                 parent: Optional[Node] = None,
                                 parent_attr: Optional[str] = None):
        name = node.decl_id.name
        if is_underscore_case(name):
            new_name = inflection.camelize(remove_preceding_underscores(name),
                                           uppercase_first_letter=True)
            new_name = sanitize_name_for_styling(new_name)
        else:
            new_name = inflection.camelize(name, uppercase_first_letter=True)
            new_name = sanitize_name_for_styling(new_name)
        self.variable_name_mapping[name] = new_name

        decl_id = node_factory.create_identifier(new_name)
        variable_declarator = node_factory.create_variable_declarator(decl_id)
        return True, [variable_declarator]


class ToSnakeCaseVisitor(VarNamingVisitor):
    def visit_VariableDeclarator(self,
                                 node: VariableDeclarator,
                                 parent: Optional[Node] = None,
                                 parent_attr: Optional[str] = None):
        name = node.decl_id.name
        if is_underscore_case(name):
            new_name = inflection.underscore(remove_preceding_underscores(name))
            new_name = sanitize_name_for_styling(new_name)
        else:
            new_name = inflection.underscore(name)
            new_name = sanitize_name_for_styling(new_name)
        self.variable_name_mapping[name] = new_name

        decl_id = node_factory.create_identifier(new_name)
        variable_declarator = node_factory.create_variable_declarator(decl_id)
        return True, [variable_declarator]


class ToUnderscoreCaseVisitor(VarNamingVisitor):
    def visit_VariableDeclarator(self,
                                 node: VariableDeclarator,
                                 parent: Optional[Node] = None,
                                 parent_attr: Optional[str] = None):
        name = node.decl_id.name
        if not is_underscore_case(name):
            name = '_' + name
            new_name = inflection.underscore(name)
            new_name = sanitize_name_for_styling(new_name)
            self.variable_name_mapping[name] = new_name

            decl_id = node_factory.create_identifier(new_name)
            variable_declarator = node_factory.create_variable_declarator(decl_id)
            return True, [variable_declarator]
        else:
            return False, []

    def visit_Identifier(self,
                         node: Identifier,
                         parent: Optional[Node] = None,
                         parent_attr: Optional[str] = None):
        name = node.name
        if not is_underscore_case(name):
            name = '_' + name
            new_name = self.variable_name_mapping.get(name, None)
            if new_name is not None:
                decl_id = node_factory.create_identifier(new_name)
                return True, [decl_id]
            else:
                return False, []
        else:
            return False, []
