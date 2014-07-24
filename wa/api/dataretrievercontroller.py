from wa.api.apirequest import ApiRequest
from wa.api.apiresponse import ApiResponse
from wa.api import returncode
from wa.engine.transmissionerror import TransmissionError


class DataRetrieverController(object):
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

    def get(self, api_key_str, latitude_str, longitude_str):
        self._reset_state()

        try:
            self._get_internal(api_key_str, latitude_str, longitude_str)
        except Exception as err:
            self._return_error(returncode.UNEXPECTED_ERROR, str(err))

        return self._result()

    def _result(self):
        return ApiResponse(
            self._return_code,
            self._error_msg,
            self._summary_str,
            self._pop_percent,
            self._intensity_type,
            self._precipitation_type
        )

    def _get_internal(self, api_key_str, latitude_str, longitude_str):
        request = ApiRequest(api_key_str, latitude_str, longitude_str)
        validation_result = request.validate()

        if validation_result != returncode.OK:
            self._return_error(validation_result, "Invalid Request Parameters")
            return

        try:
            data_request = self.builder.build(request)
        except ValueError as err:
            self._return_error(returncode.ERROR_BUILDING_REQUEST, str(err))
            return

        if not self.validator.is_valid(api_key_str):
            self._return_error(returncode.INVALID_API_KEY, "Invalid Api Key")
            return

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
