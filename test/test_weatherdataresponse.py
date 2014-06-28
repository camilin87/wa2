from unittest import TestCase
from bo.weatherdataresponse import WeatherDataResponse


class TestWeatherDataResponse(TestCase):
    def test_creation(self):
        self.assertIsNotNone(WeatherDataResponse())
