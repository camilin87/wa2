from wa.api.keyvalidator import KeyValidator


class HardcodedKeys(KeyValidator):
    def is_valid(self, api_key):
        return (
            "eLMj6u65bAzYbZ7WxJszZc8E" == api_key or
            "29hrndtLxcjnAkUcnyRTnmAY" == api_key
        )
