import unittest
import numpy as np
from cluster.dbscan import DensityBasedSCAN


class TestDBSCAN(unittest.TestCase):

    def setUp(self):
        self.simple_set = np.array([[1, 2],
                                    [2, 2],
                                    [2, 3],
                                    [8, 7],
                                    [8, 8],
                                    [25, 80]])

    def simple_test(self):
        clustering = DensityBasedSCAN(epsilon = 3, min_samples= 2)
        clustering.fit(self.simple_set)
        self.assertEqual(clustering.predict(), np.array([0, 0, 0, 1, 1, -1]))


if __name__ == '__main__':
    unittest.main()