from unittest import TestCase
from wa.api.datarequestbuilder import DataRequestBuilder
from wa.api.apirequest import ApiRequest


class TestDataRequestBuilder(TestCase):
    def setUp(self):
        self.builder = DataRequestBuilder()

    def test_can_be_created(self):
        self.assertIsNotNone(self.builder)

    def test_raises_value_error_for_invalid_request(self):
        request = ApiRequest(None, None, None)
        with self.assertRaises(ValueError):
            self.builder.build(request)

    def test_creates_data_request(self):
        request = ApiRequest("123", "80.12", "-110.30")

        data_request = self.builder.build(request)

        self.assertEquals(80.12, data_request.latitude)
        self.assertEquals(-110.3, data_request.longitude)
