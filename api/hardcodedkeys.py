from api.keyvalidator import KeyValidator


class HardcodedKeys(KeyValidator):
    def is_valid(self, api_key):
        return False
