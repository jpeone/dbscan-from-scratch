import unittest
import numpy as np
from cluster.dbscan import DensityBasedSCAN
from sklearn.cluster import DBSCAN
import time


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
        self.rand_small = np.random.rand(20, 4)
        self.rand_med = np.random.rand(200, 5)
        self.rand_big = np.random.rand(600, 10)

        self._started_at = time.time()

    def tearDown(self):
        elapsed = time.time() - self._started_at
        print('{} ({}s)'.format(self.id(), round(elapsed, 3)))

    def test_simple_set(self):
        clustering = DensityBasedSCAN(epsilon = 3, min_samples = 2)
        clustering.fit(self.simple_set)
        np.testing.assert_array_equal(clustering.predict(), np.array([0, 0, 0, 1, 1, -1]))

    def test_simple_3d_set(self):
        clustering = DensityBasedSCAN(epsilon = 3, min_samples = 2)
        clustering.fit(self.simple_3d_set)
        np.testing.assert_array_equal(clustering.predict(), np.array([0, 0, 0, 1, 1, -1]))

    def test_random_4d(self):
        homebrew = DensityBasedSCAN(epsilon = 3, min_samples = 2)
        homebrew.fit(self.rand_small)

        scikit = DBSCAN(eps = 3, min_samples = 2)
        scikit.fit(self.rand_small)

        np.testing.assert_array_equal(homebrew.predict(), scikit.labels_)

    def test_random_5d(self):
        homebrew = DensityBasedSCAN(epsilon = 3, min_samples = 2)
        homebrew.fit(self.rand_med)

        scikit = DBSCAN(eps = 3, min_samples = 2)
        scikit.fit(self.rand_med)

        np.testing.assert_array_equal(homebrew.predict(), scikit.labels_)

    def test_random_10d(self):
        homebrew = DensityBasedSCAN(epsilon = 3, min_samples = 2)
        homebrew.fit(self.rand_big)

        scikit = DBSCAN(eps = 3, min_samples = 2)
        scikit.fit(self.rand_big)

        np.testing.assert_array_equal(homebrew.predict(), scikit.labels_)

    def test_time_comparison(self):
        start = time.time()
        homebrew = DensityBasedSCAN(epsilon = 3, min_samples = 2)
        homebrew.fit(self.rand_big)
        finish = time.time()
        hbtime = finish - start

        start = time.time()
        scikit = DBSCAN(eps = 3, min_samples = 2)
        scikit.fit(self.rand_big)
        finish = time.time()
        sktime = finish - start

        print('sklearn dbscan runtime:', sktime)
        print('my dbscan runtime:', hbtime)

    def test_valid_eps_min_samp(self):
        with self.assertRaises(ValueError): DensityBasedSCAN(epsilon = -1)
        with self.assertRaises(ValueError): DensityBasedSCAN(epsilon = 0)
        with self.assertRaises(ValueError): DensityBasedSCAN(min_samples = -1)
        with self.assertRaises(ValueError): DensityBasedSCAN(min_samples = 0)

    def test_fit_invalid_data(self):
        pass







if __name__ == '__main__':
    unittest.main()