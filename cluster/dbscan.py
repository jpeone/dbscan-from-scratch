import numpy as np

class DensityBasedSCAN(object):

    def __init__(self, epsilon = 1, min_samples = 3):
        # TODO verify that epsilon and min samples are valid
        self.epsilon = epislon
        self.min_samples = min_samples
        self._is_fit = False

    def fit(self, data):
        # TODO Verify data is sent
        self.cluster_second_pass
        self._is_fit = True

    def fit_predict(self, data):
        # TODO Verify data is sent
        self.cluster_second_pass
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

    def cluster_second_pass(self, data):

        length = data.shape[0] # how many elements are in our passed in data

        self.point_type = ['noise'] * length
        self.clusters = np.full((length, 1), -1)

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
            if len(relationship_list) >= self.min_samples:
                self.point_type[cur_index] = 'core'
                self.clusters[cur_index] = cluster_counter

                # Explore the entire cluster
                # I'm doing this with a while loop, because I may need to expand
                # my relationship_list as more relationships are found. As I
                # understand, for loops use a copy of the list for iterating
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
                        elif self._distance(pointa, pointb):
                            subset_list.append(k)

                    # Core point or border point?
                    if len(subset_list) >= self.min_samples:
                        self.point_type[clus_index] = 'core'
                        self.clusters[clus_index] = cluster_counter
                        
                        # using sets to find what new points were explored
                        diff = list(set(subset_list).difference(set(relationship_list)))

                        relationship_list.extend(diff)
                    else:
                        self.point_type[clus_index] = 'border'
                        self.clusters[clus_index] = cluster_counter

                    # fulfilling my promise
                    j += 1

                # Cluster is fully explored
                indices.remove(cur_index)
                indices.remove(relationship_list)

                cluster_counter += 1

            # Not a core point, do nothing, remove from indices list and start
            # loop over
            else:
                indices.remove(cur_index)
                continue
        

    # def cluster_first_pass(self, data):
        
    #     # I might not need this, but I think it might be cool to have
    #     self.point_type = ['noise'] * data.shape[0]

    #     # A list of clusters that each point belongs to -1 means no cluster
    #     self.clusters = np.full((data.shape[0], 1), -1)

    #     # take the first point, and compare it to all other points in the data
    #     for pointi, i in enumerate(data):

    #         # this is for keeping track of indices of points that are related
    #         # to pointi, but before we have enough relationships to designate it
    #         # a core point
    #         pre_core = []

    #         relate_counter = 0 #for keeping track of the number of relations

    #         cluster_counter = 0 #for naming new clusters

    #         for pointj, j in enumerate(data):

    #             # if at the same index, skip comparison (its the same point)
    #             if i == j:
    #                 continue

    #             # check to see if the points are within epsilon distance
    #             elif _distance(pointi, pointj) <= self.epsilon:
    #                 relate_counter += 1

    #                 # Check to see how many relations are made
    #                 # Track the less than min_samples relations
    #                 if relate_counter < self.min_samples:
    #                     pre_core.append(j)

    #                 # For exactly when you hit the min_samples and need to 
    #                 # upgrade pre_core points to be at least border
    #                 elif relate_counter == self.min_samples:
    #                     self.point_type[i] = 'core'

    #                     if self.clusters[i] >= 0:
    #                         cur_cluster = self.clusters[i]
    #                     else:
    #                         cur_cluster = cluster_counter
    #                         self.clusters[i] = cluster_counter

    #                     # realized this is moot, if a point is related to a core
    #                     # I will have already assigned it to that cluster
    #                     #
    #                     # for k in pre_core:
    #                     #     if self.point_type[k] == 'core':
    #                     #         # TODO, keep an eye on this, you may need to
    #                     #         # compare potential cur_clusters incase it 
    #                     #         # relates to multiple clusters. I suspect that
    #                     #         # will not be an issue though.
    #                     #         if self.clusters[k] < cur_cluster:
    #                     #             cur_cluster = self.clusters[k]
    #                     #     elif self.point_type[k] == 'border':
    #                     #         # TODO, keep an eye on this, I believe nothing
    #                     #         # should happen here, because two core points 
    #                     #         # could share a border point within epsilon
    #                     #         # distance, while that border point itself
    #                     #         # still hass fewer than min_samples meaning
    #                     #         # it would not impart the property of one 
    #                     #         # cluster onto another.
    #                     #         continue
                        
    #                     for k in pre_core:
    #                         if self.point_type[k] == 'noise':
    #                             self.point_type[k] = 'border'
    #                             self.clusters[k] = curr_cluster
    #                         else:

                                
    def cluster_ndimensional(self):
        pass # TODO: if I have time creat n-dimensional clustering