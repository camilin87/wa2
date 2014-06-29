from unittest import TestCase
from bo.weatherdataresponse import WeatherDataResponse
from bo import precipitationtype


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

    def test_validates_precip_intensity_min_value(self):
        with self.assertRaises(ValueError):
            WeatherDataResponse("NA", 0.0 - 0.1, 0.0)

    def test_validates_precip_intensity_should_be_numeric(self):
        with self.assertRaises(TypeError):
            WeatherDataResponse("NA", "0.0", 0.0)

    def test_pop_percent(self):
        self.assertEquals(0, WeatherDataResponse("NA", 0, 0).pop_percent)
        self.assertEquals(50, WeatherDataResponse("NA", 0, 0.5).pop_percent)
        self.assertEquals(99, WeatherDataResponse("NA", 0, 0.995).pop_percent)

    def _precip_with_intensity(self, precipitation_intensity):
        response = WeatherDataResponse("NA", precipitation_intensity, 0.0)
        return response.precipitation

    def test_no_precipitation(self):
        self.assertEquals(precipitationtype.NONE, self._precip_with_intensity(0.0))
        self.assertEquals(precipitationtype.NONE, self._precip_with_intensity(0.002 - 0.0001))

    def test_light_precipitation(self):
        self.assertEquals(precipitationtype.LIGHT, self._precip_with_intensity(0.002))
        self.assertEquals(precipitationtype.LIGHT, self._precip_with_intensity(0.1 - 0.0001))

    def test_moderate_precipitation(self):
        self.assertEquals(precipitationtype.MODERATE, self._precip_with_intensity(0.1))
        self.assertEquals(precipitationtype.MODERATE, self._precip_with_intensity(0.4 - 0.0001))

    def test_heavy_precipitation(self):
        self.assertEquals(precipitationtype.HEAVY, self._precip_with_intensity(0.4))
        self.assertEquals(precipitationtype.HEAVY, self._precip_with_intensity(10))
