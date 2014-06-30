from engine.dataretriever import DataRetriever
from forecastio import load_forecast
from bo.dataresponse import DataResponse


class ForecastIoRetriever(DataRetriever):
    def __init__(self, api_key):
        self.api_key = api_key

    def retrieve(self, weather_data_request):
        datapoint = load_forecast(
            self.api_key,
            weather_data_request.latitude,
            weather_data_request.longitude
        ).currently()
        return DataResponse(
            datapoint.summary,
            datapoint.precipIntensity,
            datapoint.precipProbability
        )
