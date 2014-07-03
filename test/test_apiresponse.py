from unittest import TestCase
from api.apiresponse import ApiResponse
from api import returncode
from engine import intensitytype
from engine import precipitationtype


class TestApiResponse(TestCase):
    def test_creation(self):
        response = ApiResponse(
            returncode.OK,
            "Please upgrade your client",
            "Rainy day",
            50,
            intensitytype.LIGHT,
            precipitationtype.SNOW
        )

        self.assertIsNotNone(response)
        self.assertEquals(str(returncode.OK), response.result)
        self.assertEquals("Please upgrade your client", response.errormsg)
        self.assertEquals("Rainy day", response.summary)
        self.assertEquals("50", response.pop)
        self.assertEquals(str(intensitytype.LIGHT), response.intensity)
        self.assertEquals(str(precipitationtype.SNOW), response.precip)

    def test_return_code_is_required(self):
        with self.assertRaises(ValueError):
            response = ApiResponse(None, "", "NA", 50, 0, 0)

    def test_return_code_should_be_an_int(self):
        with self.assertRaises(ValueError):
            response = ApiResponse("3", "", "NA", 50, 0, 0)
        with self.assertRaises(ValueError):
            response = ApiResponse(3.3, "", "NA", 50, 0, 0)
        with self.assertRaises(ValueError):
            response = ApiResponse(3.0, "", "NA", 50, 0, 0)

    def test_error_message_assumes_a_default_value(self):
        response = ApiResponse(3, None, "NA", 50, 0, 0)
        self.assertEquals("", response.errormsg)

    def test_error_message_becomes_a_string(self):
        response = ApiResponse(3, 3.1415, "NA", 50, 0, 0)
        self.assertEquals("3.1415", response.errormsg)

    def test_summary_is_required(self):
        with self.assertRaises(ValueError):
            response = ApiResponse(3, "", None, 50, 0, 0)
        with self.assertRaises(ValueError):
            response = ApiResponse(3, "", "", 50, 0, 0)

    def test_summary_becomes_a_string(self):
        response = ApiResponse(3, 3.1415, 40, 50, 0, 0)
        self.assertEquals("40", response.summary)

    def test_pop_percent_is_required(self):
        with self.assertRaises(ValueError):
            ApiResponse(3, 3.1415, 40, None, 0, 0)

    def test_pop_percent_should_be_an_int(self):
        with self.assertRaises(ValueError):
            response = ApiResponse(3, "", "NA", "50", 0, 0)
        with self.assertRaises(ValueError):
            response = ApiResponse(3, "", "NA", 50.0, 0, 0)
        with self.assertRaises(ValueError):
            response = ApiResponse(3, "", "NA", 50.3, 0, 0)

    def test_intensity_type_is_required(self):
        with self.assertRaises(ValueError):
            ApiResponse(3, 3.1415, 40, 45, None, 0)

    def test_intensity_type_should_be_an_int(self):
        with self.assertRaises(ValueError):
            response = ApiResponse(3, "", "NA", 50, 0.3, 0)
        with self.assertRaises(ValueError):
            response = ApiResponse(3, "", "NA", 50, 4.0, 0)
        with self.assertRaises(ValueError):
            response = ApiResponse(3, "", "NA", 50, "0", 0)

    def test_precipitation_type_is_required(self):
        with self.assertRaises(ValueError):
            ApiResponse(3, 3.1415, 40, 45, 0, None)

    def test_precipitation_type_should_be_an_int(self):
        with self.assertRaises(ValueError):
            response = ApiResponse(3, "", "NA", 50, 0, 0.3)
        with self.assertRaises(ValueError):
            response = ApiResponse(3, "", "NA", 50, 0, 4.0)
        with self.assertRaises(ValueError):
            response = ApiResponse(3, "", "NA", 50, 0, "0")

