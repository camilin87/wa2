from api.dataretrievercontroller import DataRetrieverController
from api.datarequestbuilder import DataRequestBuilder
from api.hardcodedkeys import HardcodedKeys


class ApiFactory(object):
    @staticmethod
    def create_data_retriever_controller(data_retriever):
        return DataRetrieverController(
            data_retriever,
            DataRequestBuilder(),
            HardcodedKeys()
        )
