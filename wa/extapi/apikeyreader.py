import abc


class ApiKeyReader(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def key(self):
        raise NotImplementedError("This is an abstract class")
