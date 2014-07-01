from bo.dataresponse import DataResponse
from bo import intensitytype


class DataResponseBuilder(object):
    def build(self, forecastio_datapoint):
        if not forecastio_datapoint.summary:
            raise ValueError("summary_str is required")

        if (
            forecastio_datapoint.precipProbability < 0.0 or
            forecastio_datapoint.precipProbability > 1.0
        ):
            raise ValueError("precipProbability out of bounds")

        if forecastio_datapoint.precipIntensity < 0.0:
            raise ValueError("precipIntensity out of bounds")

        return DataResponse(
            forecastio_datapoint.summary,
            int(forecastio_datapoint.precipProbability * 100),
            DataResponseBuilder.precipitation_type(forecastio_datapoint.precipIntensity)
        )

    @staticmethod
    def precipitation_type(precip_intensity):
        if precip_intensity < 0.002:
            return intensitytype.NONE
        if precip_intensity < 0.1:
            return intensitytype.LIGHT
        if precip_intensity < 0.4:
            return intensitytype.MODERATE
        return intensitytype.HEAVY
