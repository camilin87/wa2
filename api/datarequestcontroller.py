from api.apirequest import ApiRequest
from api.apiresponse import ApiResponse


class DataRequestController(object):
    def __init__(self, data_request_builder, key_validator):
        pass

    def get(self, api_key_str, latitude_str, longitude_str):
        request = ApiRequest(api_key_str, latitude_str, longitude_str)
        validation_result = request.validate()
        return ApiResponse(validation_result, "", "NA", -1, -1, -1)
