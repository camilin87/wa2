from api.apirequest import ApiRequest
from api.apiresponse import ApiResponse
from api import returncode
from engine.transmissionerror import TransmissionError


class DataRequestController(object):
    def __init__(self, data_retriever, data_request_builder, key_validator):
        self.retriever = data_retriever
        self.builder = data_request_builder
        self.validator = key_validator
        self._reset_state()

    def _reset_state(self):
        self._return_code = None
        self._error_msg = ""
        self._summary_str = "NA"
        self._pop_percent = -1
        self._intensity_type = -1
        self._precipitation_type = -1

        self._api_key_str = None
        self._latitude_str = None
        self._longitude_str = None

    def get(self, api_key_str, latitude_str, longitude_str):
        self._reset_state()

        self._api_key_str = api_key_str
        self._latitude_str = latitude_str
        self._longitude_str = longitude_str

        try:
            self._get_internal()
        except Exception as err:
            self._return_error(returncode.UNEXPECTED_ERROR, str(err))
        finally:
            return ApiResponse(
                self._return_code,
                self._error_msg,
                self._summary_str,
                self._pop_percent,
                self._intensity_type,
                self._precipitation_type
            )

    def _get_internal(self):
        request = ApiRequest(
            self._api_key_str,
            self._latitude_str,
            self._longitude_str
        )
        validation_result = request.validate()

        if validation_result != returncode.OK:
            self._return_error(validation_result, "Invalid Request Parameters")
            return

        data_request = None
        try:
            data_request = self.builder.build(request)
        except ValueError as err:
            self._return_error(returncode.ERROR_BUILDING_REQUEST, str(err))
            return

        if not self.validator.is_valid(self._api_key_str):
            self._return_error(returncode.INVALID_API_KEY, "Invalid Api Key")
            return

        data_response = None
        try:
            data_response = self.retriever.retrieve(data_request)            
        except TransmissionError as err:
            self._return_error(returncode.EXTERNAL_API_ERROR, str(err))
            return

        self._read_data_response_data(data_response)
        self._return_code = returncode.OK

    def _read_data_response_data(self, data_response):
        self._summary_str = data_response.summary_str
        self._pop_percent = data_response.pop_percent
        self._intensity_type = data_response.intensity
        self._precipitation_type = data_response.precipitation

    def _return_error(self, return_code, error_message):
        self._return_code = return_code
        self._error_msg = error_message
