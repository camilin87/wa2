from engine.weatherdataretriever import WeatherDataRetriever
from forecastio import load_forecast
from bo.weatherdataresponse import WeatherDataResponse


class ForecastIoRetriever(WeatherDataRetriever):
    def __init__(self, api_key):
        self.api_key = api_key

    def retrieve(self, weather_data_request):
        datapoint = load_forecast(
            self.api_key,
            weather_data_request.latitude,
            weather_data_request.longitude
        ).currently()
        return WeatherDataResponse(
            datapoint.summary,
            datapoint.precipIntensity,
            datapoint.precipProbability
        )
