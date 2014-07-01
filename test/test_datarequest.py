from unittest import TestCase
from bo.datarequest import DataRequest


class TestDataRequest(TestCase):
    def test_creation(self):
        request = DataRequest(12.34, 56.70)

        self.assertEquals(12.34, request.latitude)
        self.assertEquals(56.7, request.longitude)

    def test_validates_latitude_min_boundary(self):
        with self.assertRaises(ValueError):
            DataRequest(-90.0 - 0.1, 56.70)

    def test_validates_latitude_max_boundary(self):
        with self.assertRaises(ValueError):
            DataRequest(90.0 + 0.1, 56.70)

    def test_validates_longitude_min_boundary(self):
        with self.assertRaises(ValueError):
            DataRequest(12.34, -180.0 - 0.1)

    def test_validates_longitude_max_boundary(self):
        with self.assertRaises(ValueError):
            DataRequest(12.34, 180.0 + 0.1)

    def test_latitude_should_be_numeric(self):
        with self.assertRaises(TypeError):
            DataRequest("12.34", 180.0)

    def test_longitude_should_be_numeric(self):
        with self.assertRaises(TypeError):
            DataRequest(-90, "180.0")

    def test_str(self):
        request = DataRequest(12, -160.1)
        actual_str = str(request)

        self.assertTrue(request.__class__.__name__ in actual_str)
        self.assertTrue("latitude=12.00" in actual_str)
        self.assertTrue("longitude=-160.10" in actual_str)
