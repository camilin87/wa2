from unittest import TestCase
from unittest.mock import MagicMock
from api.datarequestcontroller import DataRequestController


class TestDataRequestController(TestCase):
    def setUp(self):
        self.builder = MagicMock()
        self.validator = MagicMock()
        self.controller = DataRequestController(self.builder, self.validator)

    def test_can_be_created(self):
        self.assertIsNotNone(self.controller)
