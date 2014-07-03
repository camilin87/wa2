from unittest import TestCase
from api.apirequest import ApiRequest


class TestApiRequest(TestCase):
    def test_creation(self):
        request = ApiRequest("api key", "234.30", "34.99")

        self.assertIsNotNone(request)
        self.assertEquals("api key", request.api_key)
        self.assertEquals("234.30", request.latitude_str)
        self.assertEquals("34.99", request.longitude_str)
