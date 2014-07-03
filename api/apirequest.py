from api import returncode
from re import match


class ApiRequest(object):
    def __init__(self, api_key, lat_str, long_str):
        self.api_key = api_key
        self.latitude_str = lat_str
        self.longitude_str = long_str

    def validate(self):
        if not self.api_key or not match(r"^[a-zA-Z0-9]{1,100}$", self.api_key):
            return returncode.PARAM_KEY_ERROR

        if not self.latitude_str or not match(r"^\-?\d{1,2}\.{1}\d{2}$", self.latitude_str):
            return returncode.PARAM_LAT_ERROR

        if not self.longitude_str or not match(r"^\-?1?\d{1,2}\.{1}\d{2}$", self.longitude_str):
            return returncode.PARAM_LONG_ERROR

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
