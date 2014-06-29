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
