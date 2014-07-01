from bo.dataresponse import DataResponse


class DataResponseBuilder(object):
    def build(self, forecastio_datapoint):
        if not forecastio_datapoint.summary:
            raise ValueError("summary_str is required")

        if (
            forecastio_datapoint.precipProbability < 0.0 or
            forecastio_datapoint.precipProbability > 1.0
        ):
            raise ValueError("precip_probability out of bounds")

        if forecastio_datapoint.precipIntensity < 0.0:
            raise ValueError("precip_intensity out of bounds")

        return DataResponse(
            forecastio_datapoint.summary,
            forecastio_datapoint.precipIntensity,
            forecastio_datapoint.precipProbability
        )
