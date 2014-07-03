class ApiResponse(object):
    def __init__(
        self,
        return_code, error_msg, summary,
        pop_percent, intensity_type, precipitation_type
    ):
        if not isinstance(return_code, int):
            raise ValueError("return_code should be an int value")

        if not error_msg:
            error_msg = ""

        self.result = str(return_code)
        self.errormsg = str(error_msg)
        self.summary = summary
        self.pop = str(pop_percent)
        self.intensity = str(intensity_type)
        self.precip = str(precipitation_type)
