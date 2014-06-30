from unittest import TestCase
from nose.plugins.attrib import attr
from extapi.citkeys import CitKeys
from factory.enginefactory import EngineFactory
from bo.datarequest import DataRequest
from forecastio import load_forecast


@attr("integration")
class TestIntegrationEngine(TestCase):
    def setUp(self):
        key_retriever = CitKeys()
        self.api_key = key_retriever.key()
        self.data_retriever = EngineFactory.create_data_retriever(key_retriever)

    def _call_api_directly(self, lat, lng):
        datapoint = load_forecast(self.api_key, lat, lng).currently()
        return {
            "summary": datapoint.summary,
            "precipIntensity": datapoint.precipIntensity,
            "precipProbability": datapoint.precipProbability
        }

    def test_retrieves_correct_data_for_hialeah(self):
        response = self.data_retriever.retrieve(DataRequest(25.86, -80.30))
        api_response = self._call_api_directly(25.86, -80.30)

        self.assertEquals(api_response["summary"], response.summary_str)
        self.assertEquals(api_response["precipIntensity"], response.precip_intensity)
        self.assertEquals(api_response["precipProbability"], response.precip_probability)
