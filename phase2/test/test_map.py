from Map import Map
import unittest


class TestMap(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMap, self).__init__(*args, **kwargs)
        self.test_map = Map(path="./test/test_map.json")

    def test_compute_edge_length1(self):
        self.assertEqual(1, round(1.00, 2))
