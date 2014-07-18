from datetime import datetime


class ApiResponse(object):
    def __init__(
            self, return_code, error_msg, summary_str, pop_percent,
            intensity_type, precipitation_type
    ):
        if not summary_str:
            raise ValueError("summary_str is required")

        ApiResponse._should_be_int("return_code", return_code)
        ApiResponse._should_be_int("pop_percent", pop_percent)
        ApiResponse._should_be_int("intensity_type", intensity_type)
        ApiResponse._should_be_int("precipitation_type", precipitation_type)

        if not error_msg:
            error_msg = ""

        self.result = str(return_code)
        self.errormsg = str(error_msg)
        self.summary = str(summary_str)
        self.pop = str(pop_percent)
        self.intensity = str(intensity_type)
        self.precip = str(precipitation_type)
        self.timestamp = datetime.utcnow().isoformat()

    @staticmethod
    def _should_be_int(param_name, param_value):
        if not isinstance(param_value, int):
            raise ValueError("{0} should be an int value".format(param_name))

    def __str__(self):
        description_format = (
            "result={0}, errormsg='{1}', summary='{2}'" +
            "pop={3}, intensity={4}, precip={5}, timestamp='{6}'"
        )
        return self.__class__.__name__ + " " + description_format.format(
            self.result,
            self.errormsg,
            self.summary,
            self.pop,
            self.intensity,
            self.precip,
            self.timestamp
        )
