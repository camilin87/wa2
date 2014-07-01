from bo import intensitytype
from bo import precipitationtype


class DataResponse(object):
    def __init__(self, summary_str, pop_percent, intensity, precipitation):
        if not summary_str:
            raise ValueError("summary_str is required")

        if pop_percent < 0.0 or pop_percent > 100.0:
            raise ValueError("pop_percent out of bounds")

        if intensity not in intensitytype.INTENSITY_TYPES:
            raise ValueError("unkown intensity")

        if precipitation not in precipitationtype.PRECIPITATION_TYPES:
            raise ValueError("unkown precipitation")

        self.summary_str = summary_str
        self.pop_percent = int(pop_percent)
        self.intensity = intensity
        self.precipitation = precipitation

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
