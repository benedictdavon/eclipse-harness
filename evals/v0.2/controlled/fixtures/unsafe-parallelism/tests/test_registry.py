import unittest

from src.registry import HANDLERS


class RegistryTests(unittest.TestCase):
    def test_registry_starts_empty(self) -> None:
        self.assertEqual(HANDLERS, {})


if __name__ == "__main__":
    unittest.main()
