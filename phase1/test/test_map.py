from Map import Map
import unittest


class TestMap(unittest.TestCase):
    def test_compute_edge_length1(self):
        test_map = Map(path="../map.json")
        self.assertEqual(
            28.88, round(test_map.compute_edge_length(test_map.edges[1]), 2)
        )

    def test_compute_edge_length2(self):
        test_map = Map(path="../map.json")
        self.assertEqual(
            57.75, round(test_map.compute_edge_length(test_map.edges[4]), 2)
        )

    def test_shortest1(self):
        test_map = Map(path="../map.json")
        self.assertEqual([1], test_map.shortest(0, 1)[0])

    def test_shortest2(self):
        test_map = Map(path="../map.json")
        self.assertEqual([1, 13, 14], test_map.shortest(0, 10)[0])
