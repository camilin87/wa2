from unittest import TestCase
from unittest.mock import patch
from webapp.appcore import AppCore
from unittest.mock import MagicMock
from wa.extapi.citkeys import CitKeys
from wa.api.freeforall import FreeForAll
import logging


class TestAppCore(TestCase):
    def setUp(self):
        self.app_core = AppCore()

    def test_creation(self):
        self.assertIsNotNone(self.app_core)

    @patch("webapp.appcore.abort")
    def test_abort_wrapper(self, abort_mock):
        self.app_core._abort_wrapper(123)
        abort_mock.assert_called_with(123)

    @patch("webapp.appcore.jsonify")
    def test_jsonify_wrapper(self, jsonify_mock):
        seeded_result = MagicMock()

        def jsonify_func(value):
            if value == 123:
                return seeded_result
            raise NotImplementedError("Calling jsonify with invalid arguments")
        jsonify_mock.side_effect = jsonify_func

        actual_result = self.app_core._jsonify_wrapper(123)

        self.assertEquals(seeded_result, actual_result)

    def test_retrieve_data_test_returns_404_when_disabled(self):
        self.app_core.disable_debug = True
        self.app_core._abort_wrapper = MagicMock()

        self.app_core.retrieve_data_test(None, None, None)

        self.app_core._abort_wrapper.assert_called_with(404)

    @patch("webapp.appcore.ApiFactory.create_dummy_response")
    def test_retrieve_data_test_returns_dummy_response(self, create_mock):
        seeded_response = MagicMock()
        expected_result = MagicMock()

        def create_response_func(lat, long):
            if (lat == 12.30 and long == 45.58):
                return seeded_response
            raise NotImplementedError("Calling create_dummy_response with invalid arguments")
        create_mock.side_effect = create_response_func

        def jsonify_func(value):
            if value == seeded_response.__dict__:
                return expected_result
            raise NotImplementedError("Calling jsonify with invalid arguments")
        self.app_core._jsonify_wrapper = MagicMock(side_effect=jsonify_func)

        result = self.app_core.retrieve_data_test("apikey", "12.3", "45.58")

        self.assertEquals(expected_result, result)

    def test_retrieve_data_staging_returns_404_when_disabled(self):
        self.app_core.disable_debug = True
        self.app_core._abort_wrapper = MagicMock()

        self.app_core.retrieve_data_staging(None, None, None)

        self.app_core._abort_wrapper.assert_called_with(404)

    @patch("webapp.appcore.EngineFactory.create_data_retriever")
    @patch("webapp.appcore.ApiFactory.create_data_retriever_controller")
    def test_retrieve_data_staging_returns_correct_response(
            self, controller_mock, data_retriever_mock
    ):
        expected_result = MagicMock()
        seeded_data_retriever = MagicMock()
        seeded_controller = MagicMock()
        seeded_response = MagicMock()

        def create_data_retriever_func(api_key_reader):
            if isinstance(api_key_reader, CitKeys):
                return seeded_data_retriever
            raise NotImplementedError("Calling create_data_retriever with invalid arguments")
        data_retriever_mock.side_effect = create_data_retriever_func

        def create_controller_func(retriever, validator):
            if retriever == seeded_data_retriever and isinstance(validator, FreeForAll):
                return seeded_controller
            raise NotImplementedError(
                "Calling create_data_retriever_controller with invalid arguments"
            )
        controller_mock.side_effect = create_controller_func

        def get_func(api_key, lat_str, long_str):
            if api_key == "apikey" and lat_str == "12.3" and long_str == "45.58":
                return seeded_response
            raise NotImplementedError("Calling get with invalid arguments")
        seeded_controller.get.side_effect = get_func

        def jsonify_func(value):
            if value == seeded_response.__dict__:
                return expected_result
            raise NotImplementedError("Calling jsonify with invalid arguments")
        self.app_core._jsonify_wrapper = MagicMock(side_effect=jsonify_func)

        result = self.app_core.retrieve_data_staging("apikey", "12.3", "45.58")

        self.assertEquals(expected_result, result)

    @patch("webapp.appcore.EngineFactory.create_data_retriever")
    @patch("webapp.appcore.ApiFactory.create_data_retriever_controller")
    def test_retrieve_data_production_returns_correct_response(
            self, controller_mock, data_retriever_mock
    ):
        expected_result = MagicMock()
        seeded_data_retriever = MagicMock()
        seeded_controller = MagicMock()
        seeded_response = MagicMock()

        def create_data_retriever_func(api_key_reader):
            if api_key_reader is None:
                return seeded_data_retriever
            raise NotImplementedError("Calling create_data_retriever with invalid arguments")
        data_retriever_mock.side_effect = create_data_retriever_func

        def create_controller_func(retriever, validator):
            if retriever == seeded_data_retriever and validator is None:
                return seeded_controller
            raise NotImplementedError(
                "Calling create_data_retriever_controller with invalid arguments"
            )
        controller_mock.side_effect = create_controller_func

        def get_func(api_key, lat_str, long_str):
            if api_key == "apikey" and lat_str == "12.3" and long_str == "45.58":
                return seeded_response
            raise NotImplementedError("Calling get with invalid arguments")
        seeded_controller.get.side_effect = get_func

        def jsonify_func(value):
            if value == seeded_response.__dict__:
                return expected_result
            raise NotImplementedError("Calling jsonify with invalid arguments")
        self.app_core._jsonify_wrapper = MagicMock(side_effect=jsonify_func)

        result = self.app_core.retrieve_data_production("apikey", "12.3", "45.58")

        self.assertEquals(expected_result, result)

    @patch("webapp.appcore.logging.basicConfig")
    def test_configures_logging(self, basic_config_mock):
        self.app_core.configure_logging()

        basic_config_mock.assert_called_with(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
