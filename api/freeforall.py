from api.keyvalidator import KeyValidator


class FreeForAll(KeyValidator):
    def is_valid(self, api_key):
        if not api_key:
            return False
        return True
