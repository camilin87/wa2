class DataResponse(object):
    def __init__(
        self,
        summary_str, pop_percent, precipitation
    ):
        if not summary_str:
            raise ValueError("summary_str is required")

        self.summary_str = summary_str
        self.pop_percent = pop_percent
        self.precipitation = precipitation

    def __str__(self):
        description_format = (
            "summary_str='{0}', " +
            "pop_percent={1}, precipitation={2}"
        )
        return self.__class__.__name__ + " " + description_format.format(
            self.summary_str,
            self.pop_percent,
            self.precipitation
        )
