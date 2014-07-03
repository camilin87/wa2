from api import returncode


class ApiRequest(object):
    def __init__(self, api_key, lat_str, long_str):
        self.api_key = api_key
        self.latitude_str = lat_str
        self.longitude_str = long_str

    def validate(self):
        if not self.api_key:
            return returncode.PARAM_KEY_ERROR
        return returncode.OK

    def __str__(self):
        description_format = (
            "api_key='{0}'" +
            "latitude_str='{1}', longitude_str='{2}'"
        )
        return self.__class__.__name__ + " " + description_format.format(
            self.api_key,
            self.latitude_str,
            self.longitude_str
        )
