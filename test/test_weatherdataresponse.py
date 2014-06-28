from unittest import TestCase
from bo.weatherdataresponse import WeatherDataResponse


class TestWeatherDataResponse(TestCase):
    def test_creation(self):
        precipitation_probability = 0.234
        precipitation_intensity = 1.3
        summary = "it will rain a fucking lot"

        response = WeatherDataResponse(
            summary,
            precipitation_intensity,
            precipitation_probability,
        )

        self.assertEquals(summary, response.summary_str)
        self.assertEquals(0.23400, response.precip_probability)
        self.assertEquals(1.3, response.precip_intensity)

    def test_summary_cannot_be_none(self):
        with self.assertRaises(ValueError):
            WeatherDataResponse(None, 0.0, 0.0)

    def test_summary_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            WeatherDataResponse("", 0.0, 0.0)

    def test_validates_pop_min_value(self):
        with self.assertRaises(ValueError):
            WeatherDataResponse("NA", 0.0, 0.0 - 0.1)

    def test_validates_pop_max_value(self):
        with self.assertRaises(ValueError):
            WeatherDataResponse("NA", 0.0, 1.0 + 0.1)

    def test_validates_pop_max_value_should_be_numeric(self):
        with self.assertRaises(TypeError):
            WeatherDataResponse("NA", 0.0, "1.0")
