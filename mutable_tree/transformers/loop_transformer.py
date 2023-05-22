from .code_transformer import AbstractCodeTransformer
from ..tree_manip.visitors import ForToWhileVisitor, WhileToForVisitor


class LoopTransformer(AbstractCodeTransformer):
    TRANSFORM_LOOP_FOR = 'LoopTransformer.for_loop'
    TRANSFORM_LOOP_WHILE = 'LoopTransformer.while_loop'

    def __init__(self) -> None:
        super().__init__()
        self.visitors = {
            self.TRANSFORM_LOOP_FOR: WhileToForVisitor(),
            self.TRANSFORM_LOOP_WHILE: ForToWhileVisitor(),
        }

    def get_available_transforms(self):
        return [self.TRANSFORM_LOOP_FOR, self.TRANSFORM_LOOP_WHILE]
