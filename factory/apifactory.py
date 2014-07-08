from api.dataretrievercontroller import DataRetrieverController
from api.datarequestbuilder import DataRequestBuilder
from api.hardcodedkeys import HardcodedKeys


class ApiFactory(object):
    @staticmethod
    def create_data_retriever_controller(data_retriever, key_validator=None):
        if not key_validator:
            key_validator = HardcodedKeys()
        return DataRetrieverController(data_retriever, DataRequestBuilder(), key_validator)
