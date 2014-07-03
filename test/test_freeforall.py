from unittest import TestCase
from api.freeforall import FreeForAll


class TestFreeForAll(TestCase):
    def test_any_key_is_valid(self):
        self.assertTrue(FreeForAll().is_valid("my key"))
        self.assertEquals(True, FreeForAll().is_valid("my key"))

    def test_null_keys_are_not_valid(self):
        self.assertFalse(FreeForAll().is_valid(None))
        self.assertEquals(False, FreeForAll().is_valid(None))

    def test_empty_keys_are_not_valid(self):
        self.assertFalse(FreeForAll().is_valid(""))
        self.assertEquals(False, FreeForAll().is_valid(""))
