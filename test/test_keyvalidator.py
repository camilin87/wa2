from unittest import TestCase
from wa.api.keyvalidator import KeyValidator


class TestKeyValidator(TestCase):
    def test_is_valid_is_abstract(self):
        with self.assertRaises(NotImplementedError):
            KeyValidator().is_valid("my key")
