from extapi.forecastioretriever import ForecastIoRetriever
from extapi.productionkeys import ProductionKeys


class EngineFactory(object):
    @classmethod
    def create_data_retriever(self):
        api_key = ProductionKeys().key()
        return ForecastIoRetriever(api_key)
