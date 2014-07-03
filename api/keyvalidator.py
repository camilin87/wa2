import abc


class KeyValidator(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def is_valid(self, api_key):
        raise NotImplementedError("This is an abstract class")
