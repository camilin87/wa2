from sys import argv
from ast import literal_eval
from requests import get
from datetime import datetime


class CacheRequestHelper(object):
    def __init__(self, url, verify_ssl):
        self.url = url
        self.verify_ssl = verify_ssl
        self.prev_response = None
        self.curr_response = None
        self.time_start_utc = None
        self.seconds = None
        self.request_count = 0

    def is_cached(self, seconds=0):
        self._record_time(seconds)

        while True:
            if self._is_timeup():
                return True

            self._read_request()
            if not self._is_cached():
                return False

        return True

    def _record_time(self, seconds):
        self.time_start_utc = datetime.utcnow()
        self.seconds = seconds

    def _is_timeup(self):
        elapsed_seconds = (datetime.utcnow() - self.time_start_utc).seconds
        return elapsed_seconds >= self.seconds

    def _read_request(self):
        self.prev_response = self.curr_response
        response = get(self.url, verify=self.verify_ssl)
        if response.status_code != 200:
            raise ValueError("Received Non OK response")

        self.curr_response = response.text
        self.request_count += 1

    def _is_cached(self):
        if not self.prev_response:
            return True
        return self.prev_response == self.curr_response


def main(args):
    url = args[1]
    cache_ttl_seconds = int(args[2])
    verify_ssl = bool(literal_eval(args[3]))
    print("Starting cache test", "url=", url, "ttl_sec=", cache_ttl_seconds)

    req_tester = CacheRequestHelper(url, verify_ssl)
    is_cached = req_tester.is_cached(cache_ttl_seconds)

    print("is_cached=" + str(is_cached), "request_count=" + str(req_tester.request_count))

if __name__ == "__main__":
    main(argv)
