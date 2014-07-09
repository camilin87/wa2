from unittest import TestCase
from nose.plugins.attrib import attr
from factory.apifactory import ApiFactory
from factory.enginefactory import EngineFactory
from extapi.citkeys import CitKeys
from api.freeforall import FreeForAll
from forecastio import load_forecast
from api import returncode 


@attr("integration")
class TestIntegrationApi(TestCase):
    def setUp(self):
        api_keys_provider = CitKeys()
        data_retriever = EngineFactory.create_data_retriever(api_keys_provider)
        key_validator = FreeForAll()
        self.controller = ApiFactory.create_data_retriever_controller(
            data_retriever, key_validator
        )

    def _call_api_directly(self, lat, lng):
        api_key = CitKeys().key()
        datapoint = load_forecast(api_key, lat, lng).currently()
        result = {
            "summary": datapoint.summary,
            "precipIntensity": datapoint.precipIntensity,
            "precipProbability": datapoint.precipProbability,
            "precipType": None
        }
        if datapoint.precipIntensity > 0:
            result["precipType"] = datapoint.precipType
        return result

    def test_retrieves_hialeah_33012_data(self):
        response = self.controller.get("123abc", "25.86", "-80.30")
        api_response = self._call_api_directly(25.86, -80.30)

        self.assertEquals(str(returncode.OK), response.result)
        self.assertEquals(api_response["summary"], response.summary)
        self.assertEquals(
            str(int(float(api_response["precipProbability"]) * 100)),
            response.pop
        )
