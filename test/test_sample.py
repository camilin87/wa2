from unittest import TestCase
from engine.sample import Sample


class TestSample(TestCase):
    def test_can_be_created(self):
        self.assertIsNotNone(Sample())
