from ..visitor import TransformingVisitor
from mutable_tree.nodes import Node
from mutable_tree.nodes import node_factory, VariableDeclarator, Identifier
from typing import Optional
import inflection


# def is_all_lowercase(name) -> bool:
#     return name.lower() == name
#
#
# def is_all_uppercase(name) -> bool:
#     return name.upper() == name
#
#
# def is_camel_case(name) -> bool:
#     if is_all_lowercase(name):
#         return False
#     if not name[0].isalpha():
#         return False
#     return inflection.camelize(name, uppercase_first_letter=False) == name
#
#
# def is_pascal_case(name) -> bool:
#     if is_all_uppercase(name):
#         return False
#     if not name[0].isalpha():
#         return False
#     return inflection.camelize(name, uppercase_first_letter=True) == name
#
#
# def is_snake_case(name) -> bool:
#     return '_' in name.strip('_')


def is_underscore_case(name) -> bool:
    return name[0] == '_' and name[1:].strip('_') != ''


class ToCamelCaseVisitor(TransformingVisitor):
    def __init__(self):
        self.__variable_name_mapping = {}

    def visit_VariableDeclarator(self,
                                 node: VariableDeclarator,
                                 parent: Optional[Node] = None,
                                 parent_attr: Optional[str] = None):
        name = node.decl_id.name
        if is_underscore_case(name):
            new_name = inflection.camelize(name[1:], uppercase_first_letter=False)
        else:
            new_name = inflection.camelize(name, uppercase_first_letter=False)
        self.__variable_name_mapping[name] = new_name

        decl_id = node_factory.create_identifier(new_name)
        variable_declarator = node_factory.create_variable_declarator(decl_id)
        return True, [variable_declarator]

    def visit_Identifier(self,
                         node: Identifier,
                         parent: Optional[Node] = None,
                         parent_attr: Optional[str] = None):
        name = node.name
        new_name = self.__variable_name_mapping.get(name, None)
        if new_name is not None:
            decl_id = node_factory.create_identifier(new_name)
            return True, [decl_id]
        else:
            return False, []


class ToPascalCaseVisitor(TransformingVisitor):
    def __init__(self):
        self.__variable_name_mapping = {}

    def visit_VariableDeclarator(self,
                                 node: VariableDeclarator,
                                 parent: Optional[Node] = None,
                                 parent_attr: Optional[str] = None):
        name = node.decl_id.name
        if is_underscore_case(name):
            new_name = inflection.camelize(name[1:], uppercase_first_letter=True)
        else:
            new_name = inflection.camelize(name, uppercase_first_letter=True)
        self.__variable_name_mapping[name] = new_name

        decl_id = node_factory.create_identifier(new_name)
        variable_declarator = node_factory.create_variable_declarator(decl_id)
        return True, [variable_declarator]

    def visit_Identifier(self,
                         node: Identifier,
                         parent: Optional[Node] = None,
                         parent_attr: Optional[str] = None):
        name = node.name
        new_name = self.__variable_name_mapping.get(name, None)
        if new_name is not None:
            decl_id = node_factory.create_identifier(new_name)
            return True, [decl_id]
        else:
            return False, []


class ToSnakeCaseVisitor(TransformingVisitor):
    def __init__(self):
        self.__variable_name_mapping = {}

    def visit_VariableDeclarator(self,
                                 node: VariableDeclarator,
                                 parent: Optional[Node] = None,
                                 parent_attr: Optional[str] = None):
        name = node.decl_id.name
        if is_underscore_case(name):
            new_name = inflection.underscore(name[1:])
        else:
            new_name = inflection.underscore(name)
        self.__variable_name_mapping[name] = new_name

        decl_id = node_factory.create_identifier(new_name)
        variable_declarator = node_factory.create_variable_declarator(decl_id)
        return True, [variable_declarator]

    def visit_Identifier(self,
                         node: Identifier,
                         parent: Optional[Node] = None,
                         parent_attr: Optional[str] = None):
        name = node.name
        new_name = self.__variable_name_mapping.get(name, None)
        if new_name is not None:
            decl_id = node_factory.create_identifier(new_name)
            return True, [decl_id]
        else:
            return False, []


class ToUnderscoreCaseVisitor(TransformingVisitor):
    def __init__(self):
        self.__variable_name_mapping = {}

    def visit_VariableDeclarator(self,
                                 node: VariableDeclarator,
                                 parent: Optional[Node] = None,
                                 parent_attr: Optional[str] = None):
        name = node.decl_id.name
        if not is_underscore_case(name):
            name = '_' + name
            new_name = inflection.underscore(name)
            self.__variable_name_mapping[name] = new_name

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
            new_name = self.__variable_name_mapping.get(name, None)
            if new_name is not None:
                decl_id = node_factory.create_identifier(new_name)
                return True, [decl_id]
            else:
                return False, []
        else:
            return False, []
