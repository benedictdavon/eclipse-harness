import unittest

from src.sms import normalize_phone


class SmsTests(unittest.TestCase):
    def test_normalize_phone(self) -> None:
        self.assertEqual(normalize_phone("+1 (555) 0100"), "15550100")


if __name__ == "__main__":
    unittest.main()
