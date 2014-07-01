from bo.dataresponse import DataResponse


class DataResponseBuilder(object):
    def build(self, forecastio_datapoint):
        return DataResponse(
            forecastio_datapoint.summary,
            forecastio_datapoint.precipIntensity,
            forecastio_datapoint.precipProbability
        )
