from engine.dataretriever import DataRetriever
from forecastio import load_forecast
from extapi.dataresponsebuilder import DataResponseBuilder


class ForecastIoRetriever(DataRetriever):
    def __init__(self, api_key):
        self.api_key = api_key
        self.builder = DataResponseBuilder()

    def retrieve(self, data_request):
        datapoint = load_forecast(
            self.api_key,
            data_request.latitude,
            data_request.longitude
        ).currently()
        return self.builder.build(datapoint)
