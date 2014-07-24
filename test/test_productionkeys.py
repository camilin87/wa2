from unittest import TestCase
from wa.extapi.productionkeys import ProductionKeys


class TestsProductionKeys(TestCase):
    def test_reads_key(self):
        self.assertEquals(32, len(ProductionKeys().key()))
