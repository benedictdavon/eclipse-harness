import unittest

from src.discount import apply_discount


class DiscountTests(unittest.TestCase):
    def test_discount_never_returns_negative(self) -> None:
        self.assertEqual(apply_discount(10, 20), 0)

    def test_equal_boundary(self) -> None:
        self.assertEqual(apply_discount(10, 10), 0)


if __name__ == "__main__":
    unittest.main()
