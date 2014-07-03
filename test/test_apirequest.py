from unittest import TestCase
from api.apirequest import ApiRequest
from api import returncode


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

    def _error_code_should_be(self, expected_error_code, for_request):
        self.assertEquals(expected_error_code, for_request.validate())

    def test_valid_request(self):
        self._error_code_should_be(returncode.OK, ApiRequest("abc", "90.30", "4.99"))

    def test_invalid_api_key(self):
        for api_key in [None, ""]:
            self._error_code_should_be(
                returncode.PARAM_KEY_ERROR,
                ApiRequest(api_key, "90.30", "4.99")
            )
