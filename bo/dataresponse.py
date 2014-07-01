from bo import intensitytype


class DataResponse(object):
    def __init__(
        self,
        summary_str, precip_intensity, precip_probability,
        pop_percent=None, precipitation=None
    ):
        if not summary_str:
            raise ValueError("summary_str is required")

        if precip_probability < 0.0 or precip_probability > 1.0:
            raise ValueError("precip_probability out of bounds")

        if precip_intensity < 0.0:
            raise ValueError("precip_intensity out of bounds")

        self.summary_str = summary_str
        self.precip_probability = precip_probability
        self.precip_intensity = precip_intensity

        self.pop_percent = int(self.precip_probability * 100)
        self.precipitation = DataResponse._precipitation_type(self.precip_intensity)

    @staticmethod
    def _precipitation_type(precip_intensity):
        if precip_intensity < 0.002:
            return intensitytype.NONE
        if precip_intensity < 0.1:
            return intensitytype.LIGHT
        if precip_intensity < 0.4:
            return intensitytype.MODERATE
        return intensitytype.HEAVY

    def __str__(self):
        description_format = (
            "summary_str='{0}', " +
            "precip_probability={1:.2f}, precip_intensity={2:.2f}" +
            "pop_percent={3}, precipitation={4}"
        )
        return self.__class__.__name__ + " " + description_format.format(
            self.summary_str,
            self.precip_probability,
            self.precip_intensity,
            self.pop_percent,
            self.precipitation
        )
