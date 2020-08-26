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

    def __init__(self, epsilon = 1, min_samples = 3):
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
        except:
            raise Exception('Must fit data before calling predict')

    def _validate(self, data):
        if not np.issubdtype(data.dtype, np.number):
            raise TypeError('Data being passed in must be numeric')
        
        sum = np.sum(data)
        if np.isnan(sum):
            raise ValueError('Data being passed in must not contain nans')

    def _distance(self, a, b):
        return np.linalg.norm(a - b)

    def cluster(self, data):

        length = data.shape[0]

        self.point_type = ['noise'] * length
        self.clusters = np.full((length,), -1)

        # TODO: build a better datastructure for this
        indices = [i for i in range(length)]

        cluster_counter = 0

        # I promise to resolve this loop by removing elements from indices
        while len(indices) > 0:
            cur_index = indices[0]
            point1 = data[cur_index]

            relationship_list = []

            # Find all other points close to point1
            # TODO: Candidate for a function
            for i, point2 in enumerate(data):
                if i == cur_index:
                    continue
                elif self._distance(point1, point2) <= self.epsilon:
                    relationship_list.append(i)
            
            # Determine if point1 is a core point
            if len(relationship_list) >= (self.min_samples - 1):
                self.point_type[cur_index] = 'core'
                self.clusters[cur_index] = cluster_counter

                # Explore all points related to point1
                # I promise to resolve this while loop with an index iterator.
                j = 0
                while j < len(relationship_list):
                    subset_list = []
                    clus_index = relationship_list[j]
                    pointa = data[clus_index]

                    #add any points 
                    for k, pointb in enumerate(data):
                        if k == clus_index:
                            continue
                        elif self._distance(pointa, pointb) <= self.epsilon:
                            subset_list.append(k)

                    # Determine if pointa is a core point or a border point
                    if len(subset_list) >= (self.min_samples - 1):
                        self.point_type[clus_index] = 'core'
                        self.clusters[clus_index] = cluster_counter
                        
                        # using sets to find what new points were explored
                        diff = list(set(subset_list).difference(set(relationship_list) | set([cur_index])))

                        relationship_list.extend(diff)
                    else:
                        self.point_type[clus_index] = 'border'
                        self.clusters[clus_index] = cluster_counter

                    j += 1

                # Cluster is fully explored
                indices.remove(cur_index)
                for ele in relationship_list:
                    indices.remove(ele)

                cluster_counter += 1

            # Not a core point, do nothing, remove from indices list and start
            # loop over
            else:
                indices.remove(cur_index)
                continue