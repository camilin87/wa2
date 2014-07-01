from unittest import TestCase
from extapi.dataresponsebuilder import DataResponseBuilder
from mock import MagicMock


class TestDataResponseBuilder(TestCase):
    def test_creation(self):
        self.assertIsNotNone(DataResponseBuilder())

    def test_builds_response(self):
        seeded_datapoint = MagicMock()
        seeded_datapoint.summary = "some rain"
        seeded_datapoint.precipIntensity = float(0.8)
        seeded_datapoint.precipProbability = int(1)

        response = DataResponseBuilder().build(seeded_datapoint)

        self.assertEquals("some rain", response.summary_str)
        self.assertEquals(1.0, response.precip_probability)
        self.assertEquals(0.8, response.precip_intensity)
