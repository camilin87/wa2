from unittest import TestCase
from unittest.mock import MagicMock
from api.datarequestcontroller import DataRequestController
from api import returncode
from api.apirequest import ApiRequest
from api.datarequestbuilder import DataRequestBuilder


class TestDataRequestController(TestCase):
    def test_can_be_created(self):
        self.assertIsNotNone(DataRequestController(None, None, None))

    def _verify_no_data(self, api_response):
        self.assertIsNotNone(api_response.errormsg)
        self.assertNotEquals("", api_response.errormsg)
        self.assertEquals("NA", api_response.summary)
        self.assertEquals("-1", api_response.pop)
        self.assertEquals("-1", api_response.intensity)
        self.assertEquals("-1", api_response.precip)

    def test_returns_invalid_request_validation_error_code_for_api(self):
        expected_returncode = str(ApiRequest("", "12.23", "23.45").validate())
        controller = DataRequestController(None, None, None)

        response = controller.get("", "12.23", "23.45")

        self.assertEquals(expected_returncode, response.result)
        self.assertEquals("Invalid Request Parameters", response.errormsg)
        self._verify_no_data(response)

    def test_returns_invalid_request_validation_error_code_for_latitude(self):
        expected_returncode = str(ApiRequest("API", "", "23.45").validate())
        controller = DataRequestController(None, None, None)

        response = controller.get("API", "", "23.45")

        self.assertEquals(expected_returncode, response.result)
        self.assertEquals("Invalid Request Parameters", response.errormsg)
        self._verify_no_data(response)

    def test_returns_invalid_request_validation_error_code_for_longitude(self):
        expected_returncode = str(ApiRequest("API", "50.00", "23").validate())
        controller = DataRequestController(None, None, None)

        response = controller.get("API", "50.00", "23")

        self.assertEquals(expected_returncode, response.result)
        self.assertEquals("Invalid Request Parameters", response.errormsg)
        self._verify_no_data(response)

    def test_returns_error_building_request_error_code_invalid_latitude(self):
        controller = DataRequestController(None, DataRequestBuilder(), None)

        response = controller.get("apikey", "99.23", "23.45")

        self.assertEquals(str(returncode.ERROR_BUILDING_REQUEST), response.result)
        self._verify_no_data(response)

    def test_returns_error_building_request_error_code_invalid_longitude(self):
        controller = DataRequestController(None, DataRequestBuilder(), None)

        response = controller.get("apikey", "79.23", "190.45")

        self.assertEquals(str(returncode.ERROR_BUILDING_REQUEST), response.result)
        self._verify_no_data(response)

    def test_invalid_api_key(self):
        key_validator = MagicMock()
        key_validator.is_valid.return_value = False;
        controller = DataRequestController(None, DataRequestBuilder(), key_validator)

        response = controller.get("123456", "69.23", "130.45")

        self.assertEquals(str(returncode.INVALID_API_KEY), response.result)
        self.assertEquals("Invalid Api Key", response.errormsg)
        self._verify_no_data(response)
