from unittest import TestCase
from extapi.forecastioretriever import ForecastIoRetriever
from bo.datarequest import DataRequest
from mock import MagicMock
from mock import patch


class TestForecastIoRetriever(TestCase):
    @patch("extapi.forecastioretriever.load_forecast")
    def test_retrieves_weather_data(self, forecast_mock):
        def side_effect_func(api_key, lat, lng):
            print("side_effect_func")
            if api_key == "api key" and lat == 25.86 and lng == -80.3:
                seeded_datapoint = MagicMock()
                seeded_datapoint.summary = "some rain"
                seeded_datapoint.precipIntensity = float(0.8)
                seeded_datapoint.precipProbability = int(1)
                currently_mock = MagicMock()
                currently_mock.currently.return_value = seeded_datapoint
                return currently_mock
            raise ValueError("invalid api call")
        forecast_mock.side_effect = side_effect_func

        response = ForecastIoRetriever("api key").retrieve(
            DataRequest(25.86, -80.30)
        )

        self.assertEquals("some rain", response.summary_str)
        self.assertEquals(1.0, response.precip_probability)
        self.assertEquals(0.8, response.precip_intensity)
