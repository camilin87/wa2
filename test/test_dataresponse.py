from unittest import TestCase
from wa.engine.dataresponse import DataResponse
from wa.engine import intensitytype
from wa.engine import precipitationtype


class TestDataResponse(TestCase):
    def test_creation(self):
        intensity_type = intensitytype.LIGHT
        pop_percent = 45
        summary = "it will rain a fucking lot"
        precipitation_type = precipitationtype.RAIN

        response = DataResponse(
            summary,
            pop_percent,
            intensity_type,
            precipitation_type
        )

        self.assertEquals(summary, response.summary_str)
        self.assertEquals(45, response.pop_percent)
        self.assertEquals(intensitytype.LIGHT, response.intensity)
        self.assertEquals(precipitationtype.RAIN, response.precipitation)

    def test_summary_cannot_be_none(self):
        with self.assertRaises(ValueError):
            DataResponse(None, 0.0, 0.0, precipitationtype.RAIN)

    def test_summary_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            DataResponse("", 0.0, 0.0, precipitationtype.RAIN)

    def test_validates_pop_percent_min_value(self):
        with self.assertRaises(ValueError):
            DataResponse("NA", 0.0 - 0.1, 0, precipitationtype.RAIN)

    def test_validates_pop_percent_max_value(self):
        with self.assertRaises(ValueError):
            DataResponse("NA", 100 + 0.1, 0, precipitationtype.RAIN)

    def test_validates_pop_percent_value_should_be_numeric(self):
        with self.assertRaises(TypeError):
            DataResponse("NA", "1.0", 0, precipitationtype.RAIN)

    def test_truncates_pop_percent_value(self):
        self.assertEquals(96, DataResponse("NA", 96.98, 0, precipitationtype.RAIN).pop_percent)

    def test_validates_intensity(self):
        with self.assertRaises(ValueError):
            DataResponse("NA", 1.0, 5000, precipitationtype.RAIN)

    def test_validates_precipitation(self):
        with self.assertRaises(ValueError):
            DataResponse("NA", 1.0, intensitytype.HEAVY, 10000)

    def test_str(self):
        response = DataResponse("some rain", 90, intensitytype.HEAVY, precipitationtype.SNOW)
        actual_str = str(response)

        self.assertTrue(response.__class__.__name__ in actual_str)
        self.assertTrue("summary_str='some rain'" in actual_str)
        self.assertTrue("pop_percent=90" in actual_str)
        self.assertTrue(("intensity=" + str(intensitytype.HEAVY)) in actual_str)
        self.assertTrue(("precipitation=" + str(precipitationtype.SNOW)) in actual_str)
