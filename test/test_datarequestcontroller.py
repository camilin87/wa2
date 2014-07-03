from unittest import TestCase
from unittest.mock import MagicMock
from api.datarequestcontroller import DataRequestController
from api import returncode
from api.apirequest import ApiRequest


class TestDataRequestController(TestCase):
    def setUp(self):
        self.builder = MagicMock()
        self.validator = MagicMock()
        self.controller = DataRequestController(self.builder, self.validator)

    def test_can_be_created(self):
        self.assertIsNotNone(self.controller)

    def test_returns_invalid_request_validation_error_code(self):
        expected_returncode = str(ApiRequest("", "12.23", "23.45").validate())

        response = self.controller.get("", "12.23", "23.45")

        self.assertEquals(expected_returncode, response.result)
