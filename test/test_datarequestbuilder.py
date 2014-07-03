from unittest import TestCase
from api.datarequestbuilder import DataRequestBuilder


class TestDataRequestBuilder(TestCase):
    def test_can_be_created(self):
        self.assertIsNotNone(DataRequestBuilder())
