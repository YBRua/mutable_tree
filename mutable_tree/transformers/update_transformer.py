from .code_transformer import AbstractCodeTransformer
from ..tree_manip.visitors import (PrefixUpdateVisitor, PostfixUpdateVisitor,
                                   BinopUpdateVisitor, AssignUpdateVisitor)


class UpdateTransformer(AbstractCodeTransformer):
    TRANSFORM_PREFIX_UPDATE = 'UpdateTransformer.prefix_update'
    TRANSFORM_POSTFIX_UPDATE = 'UpdateTransformer.postfix_update'
    TRANSFORM_BINOP_UPDATE = 'UpdateTransformer.binop_update'
    TRANSFORM_ASSIGN_UPDATE = 'UpdateTransformer.assign_update'

    def __init__(self) -> None:
        super().__init__()
        self.visitors = {
            self.TRANSFORM_PREFIX_UPDATE: PrefixUpdateVisitor(),
            self.TRANSFORM_POSTFIX_UPDATE: PostfixUpdateVisitor(),
            self.TRANSFORM_BINOP_UPDATE: BinopUpdateVisitor(),
            self.TRANSFORM_ASSIGN_UPDATE: AssignUpdateVisitor(),
        }

    def get_available_transforms(self):
        return [
            self.TRANSFORM_PREFIX_UPDATE,
            self.TRANSFORM_POSTFIX_UPDATE,
            self.TRANSFORM_BINOP_UPDATE,
            self.TRANSFORM_ASSIGN_UPDATE,
        ]
