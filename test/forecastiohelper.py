from wa.extapi.citkeys import CitKeys
from forecastio import load_forecast
from logging import info


class ForecastIoHelper(object):
    @staticmethod
    def call_api_directly(lat, lng):
        api_key = CitKeys().key()

        info((
            "ForecastIoHelper.call_api_directly; " +
            "api_key='{0}', latitude={1:.2f}, longitude={2:.2f}"
        ).format(
            api_key,
            lat,
            lng
        ))

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
