from unittest import TestCase
from extapi.dataresponsebuilder import DataResponseBuilder
from mock import MagicMock
from mock import patch


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
