from unittest import TestCase
from wa.api.dataretrievercontroller import DataRetrieverController
from wa.factory.apifactory import ApiFactory
from unittest.mock import MagicMock
from wa.api.datarequestbuilder import DataRequestBuilder
from wa.api.hardcodedkeys import HardcodedKeys
from wa.api.apiresponse import ApiResponse


class TestEngineFactory(TestCase):
    def test_creates_data_retriever_controller(self):
        data_retriever_mock = MagicMock()

        controller = ApiFactory.create_data_retriever_controller(data_retriever_mock)

        self.assertIsInstance(controller, DataRetrieverController)
        self.assertEquals(data_retriever_mock, controller.retriever)
        self.assertIsInstance(controller.builder, DataRequestBuilder)
        self.assertIsInstance(controller.validator, HardcodedKeys)

    def test_creates_custom_data_retriever_controller(self):
        key_validator_mock = MagicMock()

        controller = ApiFactory.create_data_retriever_controller(MagicMock(), key_validator_mock)

        self.assertIsInstance(controller, DataRetrieverController)
        self.assertEquals(key_validator_mock, controller.validator)

    def test_creates_dummy_response_sunny(self):
        response = ApiFactory.create_dummy_response(45, 45)
        self.assertIsInstance(response, ApiResponse)
        self.assertTrue("Sunny" in response.summary)

    def test_creates_dummy_response_cloudy(self):
        response = ApiFactory.create_dummy_response(4, 45)
        self.assertIsInstance(response, ApiResponse)
        self.assertTrue("Cloudy" in response.summary)
