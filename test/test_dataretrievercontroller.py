from unittest import TestCase
from unittest.mock import MagicMock
from wa.api.dataretrievercontroller import DataRetrieverController
from wa.api import returncode
from wa.api.apirequest import ApiRequest
from wa.api.datarequestbuilder import DataRequestBuilder
from wa.engine.transmissionerror import TransmissionError
from wa.api.freeforall import FreeForAll
from wa.engine import intensitytype
from wa.engine import precipitationtype


class TestDataRetrieverController(TestCase):
    def test_can_be_created(self):
        self.assertIsNotNone(DataRetrieverController(None, None, None))

    def _verify_no_data(self, api_response):
        self.assertIsNotNone(api_response.errormsg)
        self.assertNotEquals("", api_response.errormsg)
        self.assertEquals("NA", api_response.summary)
        self.assertEquals("-1", api_response.pop)
        self.assertEquals("-1", api_response.intensity)
        self.assertEquals("-1", api_response.precip)

    def test_returns_invalid_request_validation_error_code_for_api(self):
        expected_returncode = str(ApiRequest("", "12.23", "23.45").validate())
        controller = DataRetrieverController(None, None, None)

        response = controller.get("", "12.23", "23.45")

        self.assertEquals(expected_returncode, response.result)
        self.assertEquals("Invalid Request Parameters", response.errormsg)
        self._verify_no_data(response)

    def test_returns_invalid_request_validation_error_code_for_latitude(self):
        expected_returncode = str(ApiRequest("API", "", "23.45").validate())
        controller = DataRetrieverController(None, None, None)

        response = controller.get("API", "", "23.45")

        self.assertEquals(expected_returncode, response.result)
        self.assertEquals("Invalid Request Parameters", response.errormsg)
        self._verify_no_data(response)

    def test_returns_invalid_request_validation_error_code_for_longitude(self):
        expected_returncode = str(ApiRequest("API", "50.00", "23").validate())
        controller = DataRetrieverController(None, None, None)

        response = controller.get("API", "50.00", "23")

        self.assertEquals(expected_returncode, response.result)
        self.assertEquals("Invalid Request Parameters", response.errormsg)
        self._verify_no_data(response)

    def test_returns_error_building_request_error_code_invalid_latitude(self):
        controller = DataRetrieverController(None, DataRequestBuilder(), None)

        response = controller.get("apikey", "99.23", "23.45")

        self.assertEquals(str(returncode.ERROR_BUILDING_REQUEST), response.result)
        self._verify_no_data(response)

    def test_returns_error_building_request_error_code_invalid_longitude(self):
        controller = DataRetrieverController(None, DataRequestBuilder(), None)

        response = controller.get("apikey", "79.23", "190.45")

        self.assertEquals(str(returncode.ERROR_BUILDING_REQUEST), response.result)
        self._verify_no_data(response)

    def test_invalid_api_key(self):
        key_validator = MagicMock()
        key_validator.is_valid.return_value = False
        controller = DataRetrieverController(None, DataRequestBuilder(), key_validator)

        response = controller.get("123456", "69.23", "130.45")

        self.assertEquals(str(returncode.INVALID_API_KEY), response.result)
        self.assertEquals("Invalid Api Key", response.errormsg)
        self._verify_no_data(response)

    def test_returns_external_api_error_on_transmission_error(self):
        transmitter = MagicMock()
        transmitter.retrieve.side_effect = TransmissionError("Transmission Timeout")
        controller = DataRetrieverController(transmitter, DataRequestBuilder(), FreeForAll())

        response = controller.get("123456", "69.23", "130.45")

        self.assertEquals(str(returncode.EXTERNAL_API_ERROR), response.result)
        self.assertEquals("Transmission Timeout", response.errormsg)
        self._verify_no_data(response)

    def test_gracefully_returns_unexpected_error(self):
        transmitter = MagicMock()
        transmitter.retrieve.side_effect = NotImplementedError("Unexpected Error")
        controller = DataRetrieverController(transmitter, DataRequestBuilder(), FreeForAll())

        response = controller.get("123456", "69.23", "130.45")

        self.assertEquals(str(returncode.UNEXPECTED_ERROR), response.result)
        self.assertEquals("Unexpected Error", response.errormsg)
        self._verify_no_data(response)

    def test_returns_retriever_result(self):
        seeded_data_request = MagicMock()

        builder_mock = MagicMock()
        builder_mock.build.return_value = seeded_data_request

        data_response = MagicMock()
        data_response.summary_str = "Hail day"
        data_response.pop_percent = 32
        data_response.intensity = intensitytype.MODERATE
        data_response.precipitation = precipitationtype.HAIL

        def retrieve_func(data_req):
            if data_req == seeded_data_request:
                return data_response
            raise NotImplementedError("Calling retrieve with invalid arguments")

        retriever_mock = MagicMock()
        retriever_mock.retrieve = MagicMock(side_effect=retrieve_func)
        controller = DataRetrieverController(retriever_mock, builder_mock, FreeForAll())

        response = controller.get("123456", "-69.23", "-130.45")

        self.assertEquals(str(returncode.OK), response.result)
        self.assertEquals("", response.errormsg)
        self.assertEquals("Hail day", response.summary)
        self.assertEquals("32", response.pop)
        self.assertEquals(str(intensitytype.MODERATE), response.intensity)
        self.assertEquals(str(precipitationtype.HAIL), response.precip)
