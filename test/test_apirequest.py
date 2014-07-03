from unittest import TestCase
from api.apirequest import ApiRequest


class TestApiRequest(TestCase):
    def test_creation(self):
        request = ApiRequest()

        self.assertIsNotNone(request)
