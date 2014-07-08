from unittest import TestCase
from api.dataretrievercontroller import DataRetrieverController
from factory.apifactory import ApiFactory
from unittest.mock import MagicMock
from api.datarequestbuilder import DataRequestBuilder
from api.hardcodedkeys import HardcodedKeys


class TestEngineFactory(TestCase):
    def test_creates_data_retriever_controller(self):
        data_retriever_mock = MagicMock()

        controller = ApiFactory.create_data_retriever_controller(data_retriever_mock)

        self.assertIsInstance(controller, DataRetrieverController)
        self.assertEquals(data_retriever_mock, controller.retriever)
        self.assertIsInstance(controller.builder, DataRequestBuilder)
        self.assertIsInstance(controller.validator, HardcodedKeys)
