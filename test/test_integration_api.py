from unittest import TestCase
from nose.plugins.attrib import attr
from factory.apifactory import ApiFactory
from factory.enginefactory import EngineFactory
from extapi.citkeys import CitKeys
from api.freeforall import FreeForAll
from api import returncode 
from forecastiohelper import ForecastIoHelper
from engine import intensitytype


@attr("integration")
class TestIntegrationApi(TestCase):
    def setUp(self):
        api_keys_provider = CitKeys()
        data_retriever = EngineFactory.create_data_retriever(api_keys_provider)
        key_validator = FreeForAll()
        self.controller = ApiFactory.create_data_retriever_controller(
            data_retriever, key_validator
        )

    def test_retrieves_hialeah_33012_data(self):
        api_response = ForecastIoHelper.call_api_directly(25.86, -80.30)

        response = self.controller.get("123abc", "25.86", "-80.30")

        self.assertEquals(str(returncode.OK), response.result)
        self.assertEquals(api_response["summary"], response.summary)
        self.assertEquals(
            str(int(float(api_response["precipProbability"]) * 100)),
            response.pop
        )
        if float(api_response["precipIntensity"]) < 0.002:
            self.assertEquals(str(intensitytype.NONE), response.intensity)
        else:
            self.assertTrue(int(response.intensity) > intensitytype.NONE)
