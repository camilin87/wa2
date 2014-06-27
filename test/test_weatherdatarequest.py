from unittest import TestCase
from bo.weatherdatarequest import WeatherDataRequest


class TestWeatherDataRequest(TestCase):
    def test_creation(self):
        self.assertIsNotNone(WeatherDataRequest(12.34, 56.70))

    def test_validates_latitude_min_boundary(self):
        with self.assertRaises(ValueError):
            WeatherDataRequest(-90.0 - 0.1, 56.70)

    def test_validates_latitude_max_boundary(self):
        with self.assertRaises(ValueError):
            WeatherDataRequest(90.0 + 0.1, 56.70)
