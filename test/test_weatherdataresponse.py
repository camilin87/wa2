from unittest import TestCase
from bo.weatherdataresponse import WeatherDataResponse


class TestWeatherDataResponse(TestCase):
    def test_creation(self):
        precipitation_probability = 2.34
        precipitation_intensity = 1.3
        summary = "it will rain a fucking lot"

        response = WeatherDataResponse(
            summary,
            precipitation_intensity,
            precipitation_probability,
        )

        self.assertEquals(summary, response.summary_str)
        self.assertEquals(2.3400, response.precip_probability)
        self.assertEquals(1.3, response.precip_intensity)

    def test_summary_must_be_specified(self):
        with self.assertRaises(ValueError):
            WeatherDataResponse(None, 0.0, 0.0)
        with self.assertRaises(ValueError):
            WeatherDataResponse("", 0.0, 0.0)
