import unittest

from src.email import normalize_subject


class EmailTests(unittest.TestCase):
    def test_normalize_subject(self) -> None:
        self.assertEqual(normalize_subject(" A   B "), "A B")


if __name__ == "__main__":
    unittest.main()
