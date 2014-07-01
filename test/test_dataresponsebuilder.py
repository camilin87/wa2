from unittest import TestCase
from extapi.dataresponsebuilder import DataResponseBuilder
from mock import MagicMock


class TestDataResponseBuilder(TestCase):
    def setUp(self):
        self.builder = DataResponseBuilder()

    def test_creation(self):
        self.assertIsNotNone(self.builder)

    def _data_point(self, summary, precipIntensity, precipProbability):
        seeded_datapoint = MagicMock()
        seeded_datapoint.summary = summary
        seeded_datapoint.precipIntensity = float(precipIntensity)
        seeded_datapoint.precipProbability = float(precipProbability)
        return seeded_datapoint

    def test_builds_response(self):
        seeded_datapoint = self._data_point("some rain", 0.8, 1)

        response = self.builder.build(seeded_datapoint)

        self.assertEquals("some rain", response.summary_str)
        self.assertEquals(1.0, response.precip_probability)
        self.assertEquals(0.8, response.precip_intensity)
