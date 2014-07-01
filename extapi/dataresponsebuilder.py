from bo.dataresponse import DataResponse
from bo import intensitytype
from bo import precipitationtype


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
            int(forecastio_datapoint.precipProbability * 100.0),
            DataResponseBuilder.intensity_type(forecastio_datapoint.precipIntensity),
            DataResponseBuilder._precipitation_type(forecastio_datapoint)
        )

    @staticmethod
    def _precipitation_type(forecastio_datapoint):
        if forecastio_datapoint.precipIntensity > 0.0:
            precipType = forecastio_datapoint.precipType
            return DataResponseBuilder.precipitation_type_from_str(precipType)
        return precipitationtype.NONE

    @staticmethod
    def precipitation_type_from_str(precipType):
        if precipType == "rain":
            return precipitationtype.RAIN
        if precipType == "snow":
            return precipitationtype.SNOW
        if precipType == "sleet":
            return precipitationtype.SLEET
        if precipType == "hail":
            return precipitationtype.HAIL
        raise ValueError("Unknown precipType={0}".format(precipType))

    @staticmethod
    def intensity_type(precip_intensity):
        if precip_intensity < 0.002:
            return intensitytype.NONE
        if precip_intensity < 0.1:
            return intensitytype.LIGHT
        if precip_intensity < 0.4:
            return intensitytype.MODERATE
        return intensitytype.HEAVY
