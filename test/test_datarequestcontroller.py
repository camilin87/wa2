from unittest import TestCase
from unittest.mock import MagicMock
from api.datarequestcontroller import DataRequestController
from api import returncode
from api.apirequest import ApiRequest
from api.datarequestbuilder import DataRequestBuilder


class TestDataRequestController(TestCase):
    def test_can_be_created(self):
        self.assertIsNotNone(DataRequestController(None, None))

    def _verify_no_data(self, api_response):
        self.assertIsNotNone(api_response.errormsg)
        self.assertNotEquals("", api_response.errormsg)
        self.assertEquals("NA", api_response.summary)
        self.assertEquals("-1", api_response.pop)
        self.assertEquals("-1", api_response.intensity)
        self.assertEquals("-1", api_response.precip)

    def test_returns_invalid_request_validation_error_code(self):
        expected_returncode = str(ApiRequest("", "12.23", "23.45").validate())
        controller = DataRequestController(None, None)

        response = controller.get("", "12.23", "23.45")

        self.assertEquals(expected_returncode, response.result)
        self.assertEquals("Invalid Request Parameters", response.errormsg)
        self._verify_no_data(response)

    def test_returns_invalid_request_validation_error_code(self):
        expected_returncode = str(ApiRequest("API", "", "23.45").validate())
        controller = DataRequestController(None, None)

        response = controller.get("API", "", "23.45")

        self.assertEquals(expected_returncode, response.result)
        self.assertEquals("Invalid Request Parameters", response.errormsg)
        self._verify_no_data(response)

    def test_returns_error_building_request_error_code_invalid_latitude(self):
        controller = DataRequestController(DataRequestBuilder(), None)

        response = controller.get("apikey", "99.23", "23.45")

        self.assertEquals(str(returncode.ERROR_BUILDING_REQUEST), response.result)
        self._verify_no_data(response)

    def test_returns_error_building_request_error_code_invalid_longitude(self):
        controller = DataRequestController(DataRequestBuilder(), None)

        response = controller.get("apikey", "99.23", "190.45")

        self.assertEquals(str(returncode.ERROR_BUILDING_REQUEST), response.result)
        self._verify_no_data(response)
