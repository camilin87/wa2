import abc


class WeatherDataRetriever(object):
    __metaclass__  = abc.ABCMeta
 
    @abc.abstractmethod
    def retrieve(self, weather_data_request):
        raise NotImplementedError("This is an abstract class")
