class ApiRequest(object):
    def __init__(self, api_key, lat_str, long_str):
        self.api_key = api_key
        self.latitude_str = lat_str
        self.longitude_str = long_str
