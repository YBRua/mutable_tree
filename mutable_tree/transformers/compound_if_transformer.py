from .code_transformer import AbstractCodeTransformer
from ..tree_manip.visitors import CompoundIfVisitor, NestedIfVisitor


class CompoundIfTransformer(AbstractCodeTransformer):
    TRANSFORM_IF_COMPOUND = 'CompoundIfTransformer.if_compound'
    TRANSFORM_IF_NESTED = 'CompoundIfTransformer.if_nested'

    def __init__(self) -> None:
        super().__init__()
        self.visitors = {
            self.TRANSFORM_IF_COMPOUND: CompoundIfVisitor(),
            self.TRANSFORM_IF_NESTED: NestedIfVisitor(),
        }

    def get_available_transforms(self):
        return [self.TRANSFORM_IF_COMPOUND, self.TRANSFORM_IF_NESTED]
