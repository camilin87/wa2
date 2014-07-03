from unittest import TestCase
from api.datarequestbuilder import DataRequestBuilder
from api.apirequest import ApiRequest


class TestDataRequestBuilder(TestCase):
    def setUp(self):
        self.builder = DataRequestBuilder()

    def test_can_be_created(self):
        self.assertIsNotNone(self.builder)

    def test_raises_value_error_for_invalid_request(self):
        request = ApiRequest(None, None, None)
        with self.assertRaises(ValueError):
            self.builder.build(request)
