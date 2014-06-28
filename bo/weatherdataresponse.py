class WeatherDataResponse(object):
    def __init__(self, summary_str, precip_intensity, precip_probability):
        if not summary_str:
            raise ValueError("summary_str is required")

        self.summary_str = summary_str
        self.precip_probability = precip_probability
        self.precip_intensity = precip_intensity
