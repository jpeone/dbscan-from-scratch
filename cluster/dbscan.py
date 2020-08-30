import numpy as np


class DensityBasedSCAN(object):
    '''
    Perform density based spacial clustering of applications with noise on a
    set of n-dimensional points.

    Params:
        epsilon - the distance that a point must fall within to make a cluster
        min_samples - the minimum number of member points to make a core point

    Methods:
        fit(data) - takes a numpy array of points in n-dimensional space and
            clusters them.
        fit_predict(data) - takes a numpy array of points in n-dimensionl space
            and clusters them and returns a numpy array of the resulting
            cluster names.
        preditct() - returns the cluster names from an already fit model

    Example:
        >>>> from cluster.dbscan import DensityBasedSCAN
        >>>> import numpy as np
        >>>> data = np.array([[1, 2],
        ...                   [2, 2],
        ...                   [2, 3],
        ...                   [8, 7],
        ...                   [8, 8],
        ...                   [25, 80]])
        >>>> clustering = DensityBasedSCAN(epsilon = 3, min_samples = 2)
        >>>> clustering.fit(data)
        >>>> clustering.predict()
        array([0, 0, 0, 1, 1, -1])
    '''

    def __init__(self, epsilon=1, min_samples=3):
        if epsilon <= 0:
            raise ValueError('Epsilon must be positive')
        if min_samples <= 1:
            raise ValueError('Minimum samples must be greater than 1')
        self.epsilon = epsilon
        self.min_samples = min_samples

    def fit(self, data):
        self._validate(data)
        self.cluster(data)

    def fit_predict(self, data):
        self.fit(data)
        return self.clusters

    def predict(self):
        try:
            return self.clusters
        except BaseException:
            raise Exception('Must fit data before calling predict')

    def _validate(self, data):
        if not np.issubdtype(data.dtype, np.number):
            raise TypeError('Data being passed in must be numeric')

        sum = np.sum(data)
        if np.isnan(sum):
            raise ValueError('Data being passed in must not contain nans')

    def _distance(self, a, b):
        return np.linalg.norm(a - b)

    def _neighbors(self, pointa, index, data):
        '''
        Finds the neighbors of a point within epsilon distance

        Params:
            pointa - the point to find neighbors for
            index - the index that point resides at
            data - the original data set passed in during fit
        Returns:
            A list of all the neighboring points
        '''

        nn = []

        for i, pointb in enumerate(data):
            if i == index:
                continue
            elif self._distance(pointa, pointb) <= self.epsilon:
                nn.append(i)

        return nn


    def cluster(self, data):

        length = data.shape[0]

        self.point_type = ['noise'] * length
        self.clusters = np.full((length,), -1)

        # TODO: build a better sctructure for this, but MVP is a list
        indices = [i for i in range(length)]

        cluster_counter = 0

        # I promise to resolve this loop by removing elements from indices
        while len(indices) > 0:
            cur_index = indices[0]
            cur_point = data[cur_index]

            cur_neighborhood = []

            # Find all other points close to cur_point
            cur_neighborhood.extend(self._neighbors(cur_point, cur_index, data))

            # Determine if cur_point is a core point
            if len(cur_neighborhood) >= (self.min_samples - 1):
                self.point_type[cur_index] = 'core'
                self.clusters[cur_index] = cluster_counter

                # Explore all points related to cur_point
                # I promise to resolve this while loop with an index iterator.
                j = 0
                while j < len(cur_neighborhood):
                    subset_neighborhood = []
                    subset_index = cur_neighborhood[j]
                    subset_point = data[subset_index]

                    # Discover any missing neighbors
                    subset_neighborhood.extend(self._neighbors(subset_point, subset_index, data))

                    # Determine if subset_point is core point or border point
                    if len(subset_neighborhood) >= (self.min_samples - 1):
                        self.point_type[subset_index] = 'core'
                        self.clusters[subset_index] = cluster_counter

                        diff = list(set(subset_neighborhood).difference(set(cur_neighborhood) | set([cur_index])))

                        cur_neighborhood.extend(diff)
                    else:
                        self.point_type[subset_index] = 'border'
                        self.clusters[subset_index] = cluster_counter

                    j += 1

                # Cluster is fully explored
                indices.remove(cur_index)
                for ele in cur_neighborhood:
                    indices.remove(ele)

                cluster_counter += 1

            # Not a core point
            else:
                indices.remove(cur_index)
                continue
