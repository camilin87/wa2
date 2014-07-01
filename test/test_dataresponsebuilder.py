from unittest import TestCase
from extapi.dataresponsebuilder import DataResponseBuilder


class TestDataResponseBuilder(TestCase):
    def test_creation(self):
        self.assertIsNotNone(DataResponseBuilder())
