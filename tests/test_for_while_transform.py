import unittest
from .transform_test_base import TransformTestBase
from tree_manip.transforms import for_to_while


class TestForToWhile(TransformTestBase):

    def test_for_to_while(self):
        code = 'for (int i = 0; i < 10; ++i) { print(i); }'
        self.check_transform(code, for_to_while)


if __name__ == '__main__':
    unittest.main()
