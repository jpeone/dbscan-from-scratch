import numpy as np

class DensityBasedSCAN(object):
    '''
    Perform DBSCAN clustering on a set of n-dimensional points.

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
        self._is_fit = False

    def fit(self, data):
        # TODO Verify data is sent
        self.cluster(data)
        self._is_fit = True

    def fit_predict(self, data):
        # TODO Verify data is sent
        self.cluster(data)
        self._is_fit = True
        return self.clusters

    def predict(self):
        if self._is_fit:
            return self.clusters
        else:
            raise Exception('Must fit data before calling predict')

    def _distance(self, a, b):
        # we are going to use the norm, so we can work with greater than 2d
        # space
        return np.linalg.norm(a - b)

    def cluster(self, data):

        length = data.shape[0] # how many elements are in our passed in data

        self.point_type = ['noise'] * length
        self.clusters = np.full((length,), -1)

        # a list of indices.  This would be better with a more robust data type
        # but I'm restricted to only native python, numpy and scipy
        # TODO: build a better datastructure for this
        indices = [i for i in range(length)]

        cluster_counter = 0 #for incrementing cluster groups

        while len(indices) > 0:
            # this number will change as I remove indices from the list at the
            # end of the loop
            cur_index = indices[0]
            point1 = data[cur_index] # take the first point from indices list

            relationship_list = []

            # compare point1 to every other point in the data
            for i, point2 in enumerate(data):
                if i == cur_index:
                    continue
                elif self._distance(point1, point2) <= self.epsilon:
                    relationship_list.append(i)
            
            # Determine if point1 is a core point
            # Minus 1 because we do not include the current point in the
            # relationship list, so we need to offset the sample size by that
            if len(relationship_list) >= (self.min_samples - 1):
                self.point_type[cur_index] = 'core'
                self.clusters[cur_index] = cluster_counter

                # Explore the entire cluster
                # I'm doing this with a while loop, because I may need to expand
                # my relationship_list as more relationships are found.
                # for loops use a copy of the list for iterating
                # and do not play nicely with this sort of behavior.
                # I promise to resolve this while loop with an index iterator.
                j = 0
                while j < len(relationship_list):
                    subset_list = []
                    clus_index = relationship_list[j]
                    pointa = data[clus_index]

                    for k, pointb in enumerate(data):
                        if k == clus_index:
                            continue
                        elif self._distance(pointa, pointb) <= self.epsilon:
                            subset_list.append(k)

                    # Core point or border point?
                    # Minus 2 because we don't include the current point in the
                    # subset list
                    if len(subset_list) >= (self.min_samples - 1):
                        self.point_type[clus_index] = 'core'
                        self.clusters[clus_index] = cluster_counter
                        
                        # using sets to find what new points were explored
                        diff = list(set(subset_list).difference(set(relationship_list) | set([cur_index])))

                        relationship_list.extend(diff)
                    else:
                        self.point_type[clus_index] = 'border'
                        self.clusters[clus_index] = cluster_counter

                    # fulfilling my promise
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
        
    def cluster_ndimensional(self):
        pass # TODO: if I have time creat n-dimensional clustering