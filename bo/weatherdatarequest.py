class WeatherDataRequest(object):
    def __init__(self, latitude, longitude):
        if latitude < -90.0 or latitude > 90.0:
            raise ValueError("Latitude out of bounds")
