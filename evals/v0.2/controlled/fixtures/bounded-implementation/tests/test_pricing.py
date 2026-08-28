import unittest

from src.pricing import calculate_total


class PricingTests(unittest.TestCase):
    def test_total(self) -> None:
        self.assertEqual(calculate_total([100, 250]), 350)

    def test_negative_amount(self) -> None:
        with self.assertRaises(ValueError):
            calculate_total([100, -1])


if __name__ == "__main__":
    unittest.main()
