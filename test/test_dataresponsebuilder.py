from unittest import TestCase
from extapi.dataresponsebuilder import DataResponseBuilder
from unittest.mock import MagicMock
from unittest.mock import patch
from bo import intensitytype
from bo import precipitationtype


class TestDataResponseBuilder(TestCase):
    def setUp(self):
        self.builder = DataResponseBuilder()

    def test_creation(self):
        self.assertIsNotNone(self.builder)

    def _data_point(
        self,
        summary, precipIntensity, precipProbability,
        precipType="rain"
    ):
        seeded_datapoint = MagicMock()
        seeded_datapoint.summary = summary
        seeded_datapoint.precipIntensity = precipIntensity
        seeded_datapoint.precipProbability = precipProbability
        seeded_datapoint.precipType = precipType
        return seeded_datapoint

    def _build_response(self, summary, precipIntensity, precipProbability):
        datapoint = self._data_point(summary, precipIntensity, precipProbability)
        return self.builder.build(datapoint)

    def test_builds_response(self):
        seeded_datapoint = self._data_point("some rain", 0.8, 1)

        response = self.builder.build(seeded_datapoint)

        self.assertEquals("some rain", response.summary_str)
        self.assertEquals(100, response.pop_percent)
        self.assertEquals(intensitytype.HEAVY, response.intensity)

    def test_summary_cannot_be_none(self):
        with self.assertRaises(ValueError):
            seeded_datapoint = self._data_point(None, 0.0, 0.0)
            self.builder.build(seeded_datapoint)

    def test_summary_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            seeded_datapoint = self._data_point("", 0.0, 0.0)
            self.builder.build(seeded_datapoint)

    def test_validates_pop_min_value(self):
        with self.assertRaises(ValueError):
            seeded_datapoint = self._data_point("NA", 0.0, 0.0 - 0.1)
            self.builder.build(seeded_datapoint)

    def test_validates_pop_max_value(self):
        with self.assertRaises(ValueError):
            seeded_datapoint = self._data_point("NA", 0.0, 1.0 + 0.1)
            self.builder.build(seeded_datapoint)

    def test_validates_pop_value_should_be_numeric(self):
        with self.assertRaises(TypeError):
            seeded_datapoint = self._data_point("NA", 0.0, "1.0")
            self.builder.build(seeded_datapoint)

    def test_validates_precip_intensity_min_value(self):
        with self.assertRaises(ValueError):
            seeded_datapoint = self._data_point("NA", 0.0 - 0.1, 0.0)
            self.builder.build(seeded_datapoint)

    def test_validates_precip_intensity_should_be_numeric(self):
        with self.assertRaises(TypeError):
            seeded_datapoint = self._data_point("NA", "0.0", 0.0)
            self.builder.build(seeded_datapoint)

    def test_pop_percent(self):
        self.assertEquals(0, self._build_response("NA", 0, 0).pop_percent)
        self.assertEquals(50, self._build_response("NA", 0, 0.5).pop_percent)
        self.assertEquals(99, self._build_response("NA", 0, 0.995).pop_percent)

    def _precip_with_intensity(self, precipitation_intensity):
        response = self._build_response("NA", precipitation_intensity, 0.0)
        return response.intensity

    def test_no_precipitation(self):
        self.assertEquals(intensitytype.NONE, self._precip_with_intensity(0.0))
        self.assertEquals(intensitytype.NONE, self._precip_with_intensity(0.002 - 0.0001))

    def test_light_precipitation(self):
        self.assertEquals(intensitytype.LIGHT, self._precip_with_intensity(0.002))
        self.assertEquals(intensitytype.LIGHT, self._precip_with_intensity(0.1 - 0.0001))

    def test_moderate_precipitation(self):
        self.assertEquals(intensitytype.MODERATE, self._precip_with_intensity(0.1))
        self.assertEquals(intensitytype.MODERATE, self._precip_with_intensity(0.4 - 0.0001))

    def test_heavy_precipitation(self):
        self.assertEquals(intensitytype.HEAVY, self._precip_with_intensity(0.4))
        self.assertEquals(intensitytype.HEAVY, self._precip_with_intensity(10))

    def test_does_not_read_precip_type_when_no_intensity(self):
        seeded_datapoint = self._data_point("Windy", 0, 1, "rain")
        response = self.builder.build(seeded_datapoint)
        self.assertEquals(precipitationtype.NONE, response.precipitation)

    def test_precipitation_is_rain(self):
        seeded_datapoint = self._data_point("Windy", 0.1, 1, "rain")
        response = self.builder.build(seeded_datapoint)
        self.assertEquals(precipitationtype.RAIN, response.precipitation)

    def test_precipitation_is_snow(self):
        seeded_datapoint = self._data_point("Windy", 0.1, 1, "snow")
        response = self.builder.build(seeded_datapoint)
        self.assertEquals(precipitationtype.SNOW, response.precipitation)

    def test_precipitation_is_sleet(self):
        seeded_datapoint = self._data_point("Windy", 0.1, 1, "sleet")
        response = self.builder.build(seeded_datapoint)
        self.assertEquals(precipitationtype.SLEET, response.precipitation)

    def test_precipitation_is_hail(self):
        seeded_datapoint = self._data_point("Windy", 0.1, 1, "hail")
        response = self.builder.build(seeded_datapoint)
        self.assertEquals(precipitationtype.HAIL, response.precipitation)

    def test_unknown_precipitation_type(self):
        seeded_datapoint = self._data_point("Windy", 0.1, 1, "lava")
        with self.assertRaises(ValueError):
            self.builder.build(seeded_datapoint)
