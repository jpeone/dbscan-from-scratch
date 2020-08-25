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
        self.simple_3d_set = np.array([[1, 2, 3],
                                    [2, 2, 4],
                                    [2, 3, 5],
                                    [8, 7, 9],
                                    [8, 8, 10],
                                    [25, 80, 90]])

    def test_simple_set(self):
        clustering = DensityBasedSCAN(epsilon = 3, min_samples = 2)
        clustering.fit(self.simple_set)
        np.testing.assert_array_equal(clustering.predict(), np.array([0, 0, 0, 1, 1, -1]))

    def test_simple_3d_set(self):
        clustering = DensityBasedSCAN(epsilon = 3, min_samples = 2)
        clustering.fit(self.simple_3d_set)
        np.testing.assert_array_equal(clustering.predict(), np.array([0, 0, 0, 1, 1, -1]))





if __name__ == '__main__':
    unittest.main()