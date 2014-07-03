from unittest import TestCase
from api.apiresponse import ApiResponse


class TestApiResponse(TestCase):
    def test_creation(self):
        response = ApiResponse()
        self.assertIsNotNone(response)
