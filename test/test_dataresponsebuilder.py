from unittest import TestCase
from extapi.dataresponsebuilder import DataResponseBuilder
from mock import MagicMock
from mock import patch
from bo import intensitytype


class TestDataResponseBuilder(TestCase):
    def setUp(self):
        self.builder = DataResponseBuilder()

    def test_creation(self):
        self.assertIsNotNone(self.builder)

    def _data_point(self, summary, precipIntensity, precipProbability):
        seeded_datapoint = MagicMock()
        seeded_datapoint.summary = summary
        seeded_datapoint.precipIntensity = precipIntensity
        seeded_datapoint.precipProbability = precipProbability
        return seeded_datapoint

    def _build_response(self, summary, precipIntensity, precipProbability):
        datapoint = self._data_point(summary, precipIntensity, precipProbability)
        return self.builder.build(datapoint)

    def test_builds_response(self):
        seeded_datapoint = self._data_point("some rain", 0.8, 1)

        response = self.builder.build(seeded_datapoint)

        self.assertEquals("some rain", response.summary_str)
        self.assertEquals(1.0, response.precip_probability)
        self.assertEquals(0.8, response.precip_intensity)

    @patch("extapi.dataresponsebuilder.DataResponse")
    def test_summary_cannot_be_none(self, data_response_mock):
        with self.assertRaises(ValueError):
            seeded_datapoint = self._data_point(None, 0.0, 0.0)
            self.builder.build(seeded_datapoint)

    @patch("extapi.dataresponsebuilder.DataResponse")
    def test_summary_cannot_be_empty(self, data_response_mock):
        with self.assertRaises(ValueError):
            seeded_datapoint = self._data_point("", 0.0, 0.0)
            self.builder.build(seeded_datapoint)

    @patch("extapi.dataresponsebuilder.DataResponse")
    def test_validates_pop_min_value(self, data_response_mock):
        with self.assertRaises(ValueError):
            seeded_datapoint = self._data_point("NA", 0.0, 0.0 - 0.1)
            self.builder.build(seeded_datapoint)

    @patch("extapi.dataresponsebuilder.DataResponse")
    def test_validates_pop_max_value(self, data_response_mock):
        with self.assertRaises(ValueError):
            seeded_datapoint = self._data_point("NA", 0.0, 1.0 + 0.1)
            self.builder.build(seeded_datapoint)

    @patch("extapi.dataresponsebuilder.DataResponse")
    def test_validates_pop_value_should_be_numeric(self, data_response_mock):
        with self.assertRaises(TypeError):
            seeded_datapoint = self._data_point("NA", 0.0, "1.0")
            self.builder.build(seeded_datapoint)

    @patch("extapi.dataresponsebuilder.DataResponse")
    def test_validates_precip_intensity_min_value(self, data_response_mock):
        with self.assertRaises(ValueError):
            seeded_datapoint = self._data_point("NA", 0.0 - 0.1, 0.0)
            self.builder.build(seeded_datapoint)

    @patch("extapi.dataresponsebuilder.DataResponse")
    def test_validates_precip_intensity_should_be_numeric(self, data_response_mock):
        with self.assertRaises(TypeError):
            seeded_datapoint = self._data_point("NA", "0.0", 0.0)
            self.builder.build(seeded_datapoint)

    def test_pop_percent(self):
        self.assertEquals(0, self._build_response("NA", 0, 0).pop_percent)
        self.assertEquals(50, self._build_response("NA", 0, 0.5).pop_percent)
        self.assertEquals(99, self._build_response("NA", 0, 0.995).pop_percent)

    def _precip_with_intensity(self, precipitation_intensity):
        response = self._build_response("NA", precipitation_intensity, 0.0)
        return response.precipitation

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
