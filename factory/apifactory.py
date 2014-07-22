from api.dataretrievercontroller import DataRetrieverController
from api.datarequestbuilder import DataRequestBuilder
from api.hardcodedkeys import HardcodedKeys
from api.apiresponse import ApiResponse
from api import returncode
from engine import intensitytype
from engine import precipitationtype


class ApiFactory(object):
    @staticmethod
    def create_data_retriever_controller(data_retriever, key_validator=None):
        if not key_validator:
            key_validator = HardcodedKeys()
        return DataRetrieverController(data_retriever, DataRequestBuilder(), key_validator)

    @staticmethod
    def create_dummy_response():
        return ApiResponse(
            returncode.OK,
            "",
            "Sunny day",
            10,
            intensitytype.LIGHT,
            precipitationtype.RAIN
        )
