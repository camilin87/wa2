from unittest import TestCase
from extapi.forecastioretriever import ForecastIoRetriever
from engine.datarequest import DataRequest
from unittest.mock import MagicMock
from unittest.mock import patch
from requests.exceptions import RequestException
from engine.transmissionerror import TransmissionError


class TestForecastIoRetriever(TestCase):
    @patch("extapi.forecastioretriever.load_forecast")
    def test_retrieves_weather_data(self, forecast_mock):
        seeded_datapoint = MagicMock()
        seeded_response = MagicMock()

        def side_effect_forecast(api_key, lat, lng):
            if api_key == "api key" and lat == 25.86 and lng == -80.3:
                currently_mock = MagicMock()
                currently_mock.currently.return_value = seeded_datapoint
                return currently_mock
            raise ValueError("invalid api call")
        forecast_mock.side_effect = side_effect_forecast

        def side_effect_build(p_datatpoint):
            if p_datatpoint == seeded_datapoint:
                return seeded_response
            raise ValueError("invalid build call")

        retriever = ForecastIoRetriever("api key")
        retriever.builder = MagicMock()
        retriever.builder.build = MagicMock(side_effect=side_effect_build)

        response = retriever.retrieve(DataRequest(25.86, -80.30))

        self.assertEquals(seeded_response, response)

    @patch("extapi.forecastioretriever.load_forecast")
    def test_wraps_ext_api_errors_with_transmission_error(self, forecast_mock):
        seeded_exception = RequestException("connection error")
        def fake_load_forecast(key, lat, lng):
            raise seeded_exception
        forecast_mock.side_effect = fake_load_forecast

        with self.assertRaises(TransmissionError) as context:
            ForecastIoRetriever("api key").retrieve(DataRequest(25.86, -80.30))

        self.assertEquals(seeded_exception, context.exception.__cause__)
        self.assertEquals("TransmissionError: connection error", str(context.exception))
