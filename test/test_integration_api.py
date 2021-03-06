from unittest import TestCase
from nose.plugins.attrib import attr
from wa.factory.apifactory import ApiFactory
from wa.factory.enginefactory import EngineFactory
from wa.extapi.citkeys import CitKeys
from wa.api.freeforall import FreeForAll
from wa.api import returncode
from forecastiohelper import ForecastIoHelper
from wa.engine import intensitytype


@attr("integration")
class TestIntegrationApi(TestCase):
    def setUp(self):
        api_keys_provider = CitKeys()
        data_retriever = EngineFactory.create_data_retriever(api_keys_provider)
        key_validator = FreeForAll()
        self.controller = ApiFactory.create_data_retriever_controller(
            data_retriever, key_validator
        )

    def _validate_api_call(self, latitude_str, longitude_str):
        api_response = ForecastIoHelper.call_api_directly(
            float(latitude_str), float(longitude_str)
        )

        response = self.controller.get("123abc", latitude_str, longitude_str)

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

    def test_retrieves_hialeah_33012_data(self):
        self._validate_api_call("25.86", "-80.30")

    def test_retrieves_seattle_98045_data(self):
        self._validate_api_call("47.43", "-121.80")
