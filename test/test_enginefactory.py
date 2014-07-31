from unittest import TestCase
from wa.factory.enginefactory import EngineFactory
from wa.extapi.forecastioretriever import ForecastIoRetriever
from unittest.mock import MagicMock
from unittest.mock import patch


class TestEngineFactory(TestCase):
    @patch("wa.factory.enginefactory.ProductionKeys", return_value=MagicMock())
    def test_creates_production_weather_data_retriever(self, keys_mock):
        keys_mock.return_value.key = MagicMock(return_value="production key")

        retriever = EngineFactory.create_data_retriever()

        self.assertIsInstance(retriever, ForecastIoRetriever)
        self.assertEquals("production key", retriever.api_key)

    def test_creates_custom_data_retriever(self):
        keys_mock = MagicMock()
        keys_mock.key.return_value = "custom key"

        retriever = EngineFactory.create_data_retriever(keys_mock)

        self.assertIsInstance(retriever, ForecastIoRetriever)
        self.assertEquals("custom key", retriever.api_key)
