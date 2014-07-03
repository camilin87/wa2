from unittest import TestCase
from unittest.mock import MagicMock
from api.datarequestcontroller import DataRequestController
from api import returncode
from api.apirequest import ApiRequest


class TestDataRequestController(TestCase):
    def test_can_be_created(self):
        self.assertIsNotNone(DataRequestController(None, None))

    def test_returns_invalid_request_validation_error_code(self):
        expected_returncode = str(ApiRequest("", "12.23", "23.45").validate())

        controller = DataRequestController(None, None)
        response = controller.get("", "12.23", "23.45")

        self.assertEquals(expected_returncode, response.result)
        self.assertEquals("Invalid Request Parameters", response.errormsg)
        self.assertEquals("NA", response.summary)
        self.assertEquals("-1", response.pop)
        self.assertEquals("-1", response.intensity)
        self.assertEquals("-1", response.precip)
