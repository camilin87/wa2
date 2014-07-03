from api import returncode
from engine.datarequest import DataRequest


class DataRequestBuilder(object):
    def build(self, api_request):
        if api_request.validate() != returncode.OK:
            raise ValueError("api_request should be valid")

        return DataRequest(
            float(api_request.latitude_str),
            float(api_request.longitude_str)
        )
