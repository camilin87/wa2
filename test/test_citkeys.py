from unittest import TestCase
from wa.extapi.citkeys import CitKeys


class TestsCitKeys(TestCase):
    def test_reads_key(self):
        self.assertEquals(32, len(CitKeys().key()))
