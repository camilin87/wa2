from sys import argv
from requests import get
from datetime import datetime


class CacheRequestHelper(object):
    def __init__(self, url):
        self.url = url
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
        response = get(self.url)
        self.curr_response = response.text
        self.request_count += 1

    def _is_cached(self):
        if not self.prev_response: 
            return True
        return self.prev_response == self.curr_response

def main(args):
    url = args[1]
    cache_ttl_seconds = int(args[2])
    print("Starting cache test", "url=", url, "ttl_sec=", cache_ttl_seconds) 

    req_tester = CacheRequestHelper(url)
    is_cached = req_tester.is_cached(cache_ttl_seconds)

    print("is_cached=", is_cached, "request_count=", req_tester.request_count)

if __name__ == "__main__":
    main(argv)
