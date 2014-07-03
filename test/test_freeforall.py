from unittest import TestCase
from api.freeforall import FreeForAll


class TestFreeForAll(TestCase):
    def _key_should_be(self, api_key, expected_valid_value):
        self.assertEquals(expected_valid_value, FreeForAll().is_valid(api_key))

    def test_any_key_is_valid(self):
        self._key_should_be("my key", True)

    def test_null_keys_are_not_valid(self):
        self._key_should_be(None, False)

    def test_empty_keys_are_not_valid(self):
        self._key_should_be("", False)
