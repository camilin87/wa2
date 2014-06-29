from unittest import TestCase
from extapi.forecastioretriever import ForecastIoRetriever
from bo.weatherdatarequest import WeatherDataRequest
from mock import MagicMock
from mock import patch


class TestForecastIoRetriever(TestCase):
    @patch("extapi.forecastioretriever.load_forecast")
    def test_retrieves_weather_data(self, forecast_mock):
        seeded_response = MagicMock()
        seeded_response.summary = "some rain"
        seeded_response.precipIntensity = float(0.8)
        seeded_response.precipProbability = int(1)

        def side_effect_func(api_key, lat, lng):
            if api_key == "api key" and lat == 25.86 and lng == -80.3:
                return seeded_response
            raise ValueError("invalid api call")
        forecast_mock.side_effect = side_effect_func

        response = ForecastIoRetriever("api key").retrieve(
            WeatherDataRequest(25.86, -80.30)
        )

        self.assertEquals("some rain", response.summary_str)
        self.assertEquals(1.0, response.precip_probability)
        self.assertEquals(0.8, response.precip_intensity)
