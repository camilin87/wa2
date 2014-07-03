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
            response = ApiResponse(None, "", "", 50, 0, 0)

    def test_return_code_should_be_an_int(self):
        with self.assertRaises(ValueError):
            response = ApiResponse("3", "", "", 50, 0, 0)
        with self.assertRaises(ValueError):
            response = ApiResponse(3.3, "", "", 50, 0, 0)
        with self.assertRaises(ValueError):
            response = ApiResponse(3.0, "", "", 50, 0, 0)
