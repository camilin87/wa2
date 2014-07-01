from unittest import TestCase
from bo.dataresponse import DataResponse
from bo import intensitytype


class TestDataResponse(TestCase):
    def test_creation(self):
        precipitation_probability = 0.234
        precipitation_intensity = 1.3
        summary = "it will rain a fucking lot"

        response = DataResponse(
            summary,
            precipitation_intensity,
            precipitation_probability,
        )

        self.assertEquals(summary, response.summary_str)
        self.assertEquals(0.23400, response.precip_probability)
        self.assertEquals(1.3, response.precip_intensity)

    def test_summary_cannot_be_none(self):
        with self.assertRaises(ValueError):
            DataResponse(None, 0.0, 0.0)

    def test_summary_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            DataResponse("", 0.0, 0.0)

    def test_validates_pop_min_value(self):
        with self.assertRaises(ValueError):
            DataResponse("NA", 0.0, 0.0 - 0.1)

    def test_validates_pop_max_value(self):
        with self.assertRaises(ValueError):
            DataResponse("NA", 0.0, 1.0 + 0.1)

    def test_validates_pop_max_value_should_be_numeric(self):
        with self.assertRaises(TypeError):
            DataResponse("NA", 0.0, "1.0")

    def test_validates_precip_intensity_min_value(self):
        with self.assertRaises(ValueError):
            DataResponse("NA", 0.0 - 0.1, 0.0)

    def test_validates_precip_intensity_should_be_numeric(self):
        with self.assertRaises(TypeError):
            DataResponse("NA", "0.0", 0.0)

    def test_pop_percent(self):
        self.assertEquals(0, DataResponse("NA", 0, 0).pop_percent)
        self.assertEquals(50, DataResponse("NA", 0, 0.5).pop_percent)
        self.assertEquals(99, DataResponse("NA", 0, 0.995).pop_percent)

    def _precip_with_intensity(self, precipitation_intensity):
        response = DataResponse("NA", precipitation_intensity, 0.0)
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

    def test_str(self):
        response = DataResponse("some rain", 0.5, 0.9)
        actual_str = str(response)

        self.assertTrue(response.__class__.__name__ in actual_str)
        self.assertTrue("summary_str='some rain'" in actual_str)
        self.assertTrue("precip_probability=0.90" in actual_str)
        self.assertTrue("precip_intensity=0.50" in actual_str)
        self.assertTrue("pop_percent=90" in actual_str)
        self.assertTrue(("precipitation=" + str(intensitytype.HEAVY)) in actual_str)
