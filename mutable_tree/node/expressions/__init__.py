from .expression import Expression
from .array_access import ArrayAccess
from .array_expr import ArrayExpression
from .assignment_expr import AssignmentExpression, get_assignment_op, AssignmentOps
from .binary_expr import BinaryExpression, get_binary_op, BinaryOps
from .call_expr import CallExpression
from .cast_expr import CastExpression
from .field_access import FieldAccess
from .identifier import Identifier
from .instanceof_expr import InstanceofExpression
from .literal import Literal
from .new_expr import NewExpression
from .ternary_expr import TernaryExpression
from .this import ThisExpression
from .unary_expr import UnaryExpression, get_unary_op, UnaryOps
from .update_expr import UpdateExpression, get_update_op, UpdateOps

from typing import Union

PrimaryExpression = Union[Literal, Identifier, ThisExpression, NewExpression,
                          CallExpression, FieldAccess, ArrayAccess]
