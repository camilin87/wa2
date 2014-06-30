import abc


class DataRetriever(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def retrieve(self, data_request):
        raise NotImplementedError("This is an abstract class")
