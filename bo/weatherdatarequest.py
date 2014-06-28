class WeatherDataRequest(object):
    def __init__(self, latitude, longitude):
        if latitude < -90.0 or latitude > 90.0:
            raise ValueError("latitude out of bounds")

        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("longitude out of bounds")

        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        description_format = ("latitude={0:.2f}, longitude={1:.2f}")
        return self.__class__.__name__ + " " + description_format.format(
            self.latitude,
            self.longitude
        )
