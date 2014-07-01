from unittest import TestCase
from bo.dataresponse import DataResponse
from bo import intensitytype


class TestDataResponse(TestCase):
    def test_creation(self):
        intensity_type = intensitytype.LIGHT
        pop_percent = 45
        summary = "it will rain a fucking lot"

        response = DataResponse(
            summary,
            pop_percent,
            intensity_type,
        )

        self.assertEquals(summary, response.summary_str)
        self.assertEquals(45, response.pop_percent)
        self.assertEquals(intensitytype.LIGHT, response.intensity)

    def test_summary_cannot_be_none(self):
        with self.assertRaises(ValueError):
            DataResponse(None, 0.0, 0.0)

    def test_summary_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            DataResponse("", 0.0, 0.0)

    def test_str(self):
        response = DataResponse("some rain", 90, intensitytype.HEAVY)
        actual_str = str(response)

        self.assertTrue(response.__class__.__name__ in actual_str)
        self.assertTrue("summary_str='some rain'" in actual_str)
        self.assertTrue("pop_percent=90" in actual_str)
        self.assertTrue(("intensity=" + str(intensitytype.HEAVY)) in actual_str)
