from extapi.apikeyreader import ApiKeyReader


class ProductionKeys(ApiKeyReader):
    def key(self):
        # wa2_prod@cash-productions.com
        return "4ce78e2fdeca946a94c04bb76de9d3f1"
