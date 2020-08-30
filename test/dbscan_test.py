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
        self.rand_small = np.random.randint(-100, 100, size=(20, 4))
        self.rand_med = np.random.randint(-500, 500, size=(200, 5))
        self.rand_big = np.random.randint(-1000, 1000, size=(600, 10))

        self._started_at = time.time()

    def tearDown(self):
        # print out test timing after running each test
        elapsed = time.time() - self._started_at
        print('{} ({}s)'.format(self.id(), round(elapsed, 3)))

    def test_simple_set(self):
        clustering = DensityBasedSCAN(epsilon=3, min_samples=2)
        clustering.fit(self.simple_set)
        np.testing.assert_array_equal(
            clustering.predict(), np.array([0, 0, 0, 1, 1, -1]))

    def test_simple_3d_set(self):
        clustering = DensityBasedSCAN(epsilon=3, min_samples=2)
        clustering.fit(self.simple_3d_set)
        np.testing.assert_array_equal(
            clustering.predict(), np.array([0, 0, 0, 1, 1, -1]))

    def test_random_4d(self):
        homebrew = DensityBasedSCAN(epsilon=3, min_samples=2)
        homebrew.fit(self.rand_small)

        scikit = DBSCAN(eps=3, min_samples=2)
        scikit.fit(self.rand_small)

        np.testing.assert_array_equal(homebrew.predict(), scikit.labels_)

    def test_random_5d(self):
        homebrew = DensityBasedSCAN(epsilon=4, min_samples=4)
        homebrew.fit(self.rand_med)

        scikit = DBSCAN(eps=4, min_samples=4)
        scikit.fit(self.rand_med)

        np.testing.assert_array_equal(homebrew.predict(), scikit.labels_)

    def test_random_10d(self):
        homebrew = DensityBasedSCAN(epsilon=4, min_samples=5)
        homebrew.fit(self.rand_big)

        scikit = DBSCAN(eps=4, min_samples=5)
        scikit.fit(self.rand_big)

        np.testing.assert_array_equal(homebrew.predict(), scikit.labels_)

    def test_time_comparison(self):
        start = time.time()
        homebrew = DensityBasedSCAN(epsilon=3, min_samples=2)
        homebrew.fit(self.rand_big)
        finish = time.time()
        hbtime = finish - start

        start = time.time()
        scikit = DBSCAN(eps=3, min_samples=2)
        scikit.fit(self.rand_big)
        finish = time.time()
        sktime = finish - start

        print()
        print('Time Comparison: Spatial Indexing vs List indexing')
        print('--------------------------------------------------------------')
        print('sklearn dbscan runtime:', sktime)
        print('my dbscan runtime:', hbtime)
        print('--------------------------------------------------------------')

    def test_valid_eps_min_samp(self):
        with self.assertRaises(ValueError):
            DensityBasedSCAN(epsilon=-1)
        with self.assertRaises(ValueError):
            DensityBasedSCAN(epsilon=0)
        with self.assertRaises(ValueError):
            DensityBasedSCAN(min_samples=-1)
        with self.assertRaises(ValueError):
            DensityBasedSCAN(min_samples=0)

    def test_fit_invalid_data(self):
        all_nan = np.empty([4, 4])
        all_nan[:] = np.nan
        some_nan = np.array([[1, 2, 3], [4, np.nan, 5], [6, 7, 8]])
        all_str = np.array([['this'], ['is'], ['an array'], ['of'], ['strs']])
        some_str = np.array([[1, 2, 'oops a string'], [3, 4, 5], [6, 7, 8]])

        clustering = DensityBasedSCAN()

        with self.assertRaises(ValueError):
            clustering.fit(all_nan)
        with self.assertRaises(ValueError):
            clustering.fit(some_nan)
        with self.assertRaises(TypeError):
            clustering.fit(all_str)
        with self.assertRaises(TypeError):
            clustering.fit(some_str)

    def test_predict_unfit_predict(self):
        with self.assertRaises(Exception):
            DensityBasedSCAN().predict()


if __name__ == '__main__':
    unittest.main()
