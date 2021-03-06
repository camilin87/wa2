from unittest import TestCase
from wa.engine.dataretriever import DataRetriever


class TestDataRetriever(TestCase):
    def test_retrieve_is_abstract(self):
        with self.assertRaises(NotImplementedError):
            DataRetriever().retrieve(None)
