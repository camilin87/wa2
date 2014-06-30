from extapi.forecastioretriever import ForecastIoRetriever
from extapi.productionkeys import ProductionKeys


class EngineFactory(object):
    @classmethod
    def create_data_retriever(self, api_key_reader=None):
        if not api_key_reader:
            api_key_reader = ProductionKeys()
        return ForecastIoRetriever(api_key_reader.key())