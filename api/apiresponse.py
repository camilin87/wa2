class ApiResponse(object):
    def __init__(
        self,
        return_code, error_msg, summary_str,
        pop_percent, intensity_type, precipitation_type
    ):
        if not isinstance(return_code, int):
            raise ValueError("return_code should be an int value")

        if not error_msg:
            error_msg = ""

        if not summary_str:
            raise ValueError("summary_str is required")

        if not isinstance(pop_percent, int):
            raise ValueError("pop_percent should be an int value")

        self.result = str(return_code)
        self.errormsg = str(error_msg)
        self.summary = str(summary_str)
        self.pop = str(pop_percent)
        self.intensity = str(intensity_type)
        self.precip = str(precipitation_type)
