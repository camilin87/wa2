from wa.api.keyvalidator import KeyValidator


class HardcodedKeys(KeyValidator):
    def is_valid(self, api_key):
        return (
            "4ce78e2fdeca946a94c04bb76de9d3f1" == api_key or
            "4f8ae30039c63cb663a360282c28095d" == api_key
        )
