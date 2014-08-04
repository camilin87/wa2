from unittest import TestCase
from unittest.mock import patch
from webapp.appcore import AppCore


class TestAppCore(TestCase):
    def setUp(self):
        self.app_core = AppCore()

    def test_creation(self):
        self.assertIsNotNone(self.app_core)

    @patch("webapp.appcore.abort")
    def test_abort_wrapper(self, abort_mock):
        self.app_core._abort_wrapper(123)
        abort_mock.assert_called_with(123)