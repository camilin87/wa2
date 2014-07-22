from unittest import TestCase
from api.dataretrievercontroller import DataRetrieverController
from factory.apifactory import ApiFactory
from unittest.mock import MagicMock
from api.datarequestbuilder import DataRequestBuilder
from api.hardcodedkeys import HardcodedKeys
from api.apiresponse import ApiResponse


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

    def test_creates_dummy_response(self):
        response = ApiFactory.create_dummy_response()
        self.assertIsInstance(response, ApiResponse)
