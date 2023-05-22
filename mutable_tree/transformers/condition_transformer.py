from .code_transformer import AbstractCodeTransformer
from ..tree_manip.visitors import SwitchToIfVisitor, TernaryToIfVisitor


class ConditionTransformer(AbstractCodeTransformer):
    TRANSFORM_COND_SWITCH = 'ConditionTransformer.switch'
    TRANSFORM_COND_TERNARY = 'ConditionTransformer.ternary'

    def __init__(self) -> None:
        super().__init__()
        self.visitors = {
            self.TRANSFORM_COND_SWITCH: SwitchToIfVisitor(),
            self.TRANSFORM_COND_TERNARY: TernaryToIfVisitor(),
        }

    def get_available_transforms(self):
        return [self.TRANSFORM_COND_SWITCH, self.TRANSFORM_COND_TERNARY]
