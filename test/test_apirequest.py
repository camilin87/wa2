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
        for api_key in [None, "", "a"*101]:
            self._error_code_should_be(
                returncode.PARAM_KEY_ERROR,
                ApiRequest(api_key, "90.30", "4.99")
            )

    def test_invalid_latitude(self):
        invalid_coordinates = [
            None, "", "a", "2"*101, "-2", "-90.211", "99.0", "3.99.99", "-6.9", "-101.00"
        ]
        for latitude in invalid_coordinates:
            self._error_code_should_be(
                returncode.PARAM_LAT_ERROR,
                ApiRequest("abc", latitude, "4.99")
            )

    def test_invalid_longitude(self):
        invalid_coordinates = [
            None, "", "a", "2"*101, "-2", "-90.211", "99.0", "3.99.99", "-6.9", "-201.00"
        ]
        for longitude in invalid_coordinates:
            self._error_code_should_be(
                returncode.PARAM_LONG_ERROR,
                ApiRequest("abc", "4.99", longitude)
            )
