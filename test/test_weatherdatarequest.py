from unittest import TestCase
from bo.weatherdatarequest import WeatherDataRequest


class TestWeatherDataRequest(TestCase):
    def test_creation(self):
        self.assertIsNotNone(WeatherDataRequest())
