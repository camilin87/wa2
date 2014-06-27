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

    def test_validates_longitude_min_boundary(self):
        with self.assertRaises(ValueError):
            WeatherDataRequest(12.34, -180.0 - 0.1)

    def test_validates_longitude_max_boundary(self):
        with self.assertRaises(ValueError):
            WeatherDataRequest(12.34, 180.0 + 0.1)

    def test_latitude_should_be_numeric(self):
        with self.assertRaises(TypeError):
            WeatherDataRequest("12.34", 180.0)

    def test_longitude_should_be_numeric(self):
        with self.assertRaises(TypeError):
            WeatherDataRequest(-90, "180.0")
