from wa.api.dataretrievercontroller import DataRetrieverController
from wa.api.datarequestbuilder import DataRequestBuilder
from wa.api.hardcodedkeys import HardcodedKeys
from wa.api.apiresponse import ApiResponse
from wa.api import returncode
from wa.engine import intensitytype
from wa.engine import precipitationtype


class ApiFactory(object):
    @staticmethod
    def create_data_retriever_controller(data_retriever, key_validator=None):
        if not key_validator:
            key_validator = HardcodedKeys()
        return DataRetrieverController(data_retriever, DataRequestBuilder(), key_validator)

    @staticmethod
    def create_dummy_response(latitude, longitude):
        summary_str = "Sunny Day"
        if latitude < 40:
            summary_str = "Cloudy Day"

        return ApiResponse(
            returncode.OK,
            "",
            summary_str,
            10,
            intensitytype.LIGHT,
            precipitationtype.RAIN
        )
