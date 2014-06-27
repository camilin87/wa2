from unittest import TestCase
from datetime import datetime
from datetime import tzinfo
from datetime import timezone
import time as Time
from time import strptime
from dateutil.tz import tzlocal


class TestApiCharacterization(TestCase):
    def test_time_param_value_conversion_to_unix_time(self):
        start_of_time_utc = datetime(1970, 1, 1, hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
        start_of_time_local = datetime(1970, 1, 1, hour=0, minute=0, second=0, microsecond=0, tzinfo=tzlocal())
        expected_difference = (start_of_time_local - start_of_time_utc).total_seconds()

        seconds_representation = int(Time.mktime(start_of_time_local.timetuple()))

        self.assertEquals(expected_difference, seconds_representation)

    def test_time_truncating_to_hour(self):
        expected_datetime = datetime(*strptime("2014-02-02T10:00:00", "%Y-%m-%dT%H:%M:%S")[0:6])

        current_time = datetime(*strptime("2014-02-02T10:30:00", "%Y-%m-%dT%H:%M:%S")[0:6])
        current_time = current_time.replace(minute=0, second=0, microsecond=0)

        self.assertEquals(expected_datetime, current_time);
