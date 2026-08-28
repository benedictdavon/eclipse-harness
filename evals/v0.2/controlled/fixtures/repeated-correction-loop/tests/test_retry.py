import unittest

from src.retry import retry_delay


class RetryTests(unittest.TestCase):
    def test_sequence(self) -> None:
        self.assertEqual([retry_delay(i) for i in (1, 2, 3)], [1, 2, 4])

    def test_upper_bound(self) -> None:
        with self.assertRaises(ValueError):
            retry_delay(9)


if __name__ == "__main__":
    unittest.main()
