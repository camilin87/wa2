class WeatherDataRequest(object):
    def __init__(self, latitude, longitude):
        if latitude < -90.0 or latitude > 90.0:
            raise ValueError("latitude out of bounds")

        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("longitude out of bounds")
