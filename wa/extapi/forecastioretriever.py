from wa.engine.dataretriever import DataRetriever
from forecastio import load_forecast
from wa.extapi.dataresponsebuilder import DataResponseBuilder
from requests.exceptions import RequestException
from wa.engine.transmissionerror import TransmissionError


class ForecastIoRetriever(DataRetriever):
    def __init__(self, api_key):
        self.api_key = api_key
        self.builder = DataResponseBuilder()

    def retrieve(self, data_request):
        try:
            datapoint = load_forecast(
                self.api_key,
                data_request.latitude,
                data_request.longitude
            ).currently()
            return self.builder.build(datapoint)
        except RequestException as req_error:
            raise TransmissionError("TransmissionError: " + str(req_error)) from req_error
