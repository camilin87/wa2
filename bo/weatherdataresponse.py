from bo import precipitationtype


class WeatherDataResponse(object):
    def __init__(self, summary_str, precip_intensity, precip_probability):
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
        self.precipitation = WeatherDataResponse._precipitation_type(self.precip_intensity)

    @staticmethod
    def _precipitation_type(precip_intensity):
        if precip_intensity < 0.002:
            return precipitationtype.NONE
        if precip_intensity < 0.1:
            return precipitationtype.LIGHT
        if precip_intensity < 0.4:
            return precipitationtype.MODERATE
        return precipitationtype.HEAVY
