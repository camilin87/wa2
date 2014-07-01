from bo import intensitytype
from bo import precipitationtype


class DataResponse(object):
    def __init__(self, summary_str, pop_percent, intensity, precipitation):
        DataResponse._validate_summary_str(summary_str)
        DataResponse._validate_pop_percent(pop_percent)
        DataResponse._validate_intensity(intensity)
        DataResponse._validate_precipitation(precipitation)

        self.summary_str = summary_str
        self.pop_percent = int(pop_percent)
        self.intensity = intensity
        self.precipitation = precipitation

    @staticmethod
    def _validate_summary_str(summary_str):
        if not summary_str:
            raise ValueError("summary_str is required")

    @staticmethod
    def _validate_pop_percent(pop_percent):
        if pop_percent < 0.0 or pop_percent > 100.0:
            raise ValueError("pop_percent out of bounds")

    @staticmethod
    def _validate_intensity(intensity):
        if intensity not in intensitytype.INTENSITY_TYPES:
            raise ValueError("unkown intensity")

    @staticmethod
    def _validate_precipitation(precipitation):
        if precipitation not in precipitationtype.PRECIPITATION_TYPES:
            raise ValueError("unkown precipitation")

    def __str__(self):
        description_format = (
            "summary_str='{0}', " +
            "pop_percent={1}, intensity={2}, precipitation={3}"
        )
        return self.__class__.__name__ + " " + description_format.format(
            self.summary_str,
            self.pop_percent,
            self.intensity,
            self.precipitation
        )
