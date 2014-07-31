from wa.extapi.citkeys import CitKeys
from forecastio import load_forecast


class ForecastIoHelper(object):
    @staticmethod
    def call_api_directly(lat, lng):
        api_key = CitKeys().key()
        datapoint = load_forecast(api_key, lat, lng).currently()
        result = {
            "summary": datapoint.summary,
            "precipIntensity": datapoint.precipIntensity,
            "precipProbability": datapoint.precipProbability,
            "precipType": None
        }
        if datapoint.precipIntensity > 0:
            result["precipType"] = datapoint.precipType
        return result
