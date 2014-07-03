from unittest import TestCase
from api.apirequest import ApiRequest


class TestApiRequest(TestCase):
    def test_creation(self):
        request = ApiRequest("api key", "234.30", "34.99")

        self.assertIsNotNone(request)
        self.assertEquals("api key", request.api_key)
        self.assertEquals("234.30", request.latitude_str)
        self.assertEquals("34.99", request.longitude_str)

    def test_str(self):
        request = ApiRequest("api key", "90.30", "4.99")

        actual_str = str(request)

        self.assertTrue(request.__class__.__name__ in actual_str)
        self.assertTrue("api_key='api key'" in actual_str)
        self.assertTrue("latitude_str='90.30'" in actual_str)
        self.assertTrue("longitude_str='4.99'" in actual_str)
