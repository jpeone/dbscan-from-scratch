import numpy as np


class DensityBasedSCAN(Object):

    def __init__(self, epsilon = 1, min_samples = 3):
        self.epsilon = epislon
        self.min_samples = min_samples

    def fit(self, data):
        self.clusters = self.cluster2D(data) # TODO: fitting without returning clusters

    def fit_predict(self, data):
        pass # TODO: fitting, and returns clusters

    def predict(self):
        pass # TODO: maybe this is just returning clusters for only fit data

    def _distance(self, a, b):
        # we are going to use the norm, so we can work with greater than 2d
        # space

        return np.linalg.norm(a - b)


    def cluster2D(self, data):
        
        # I might not need this, but I think it might be cool to have
        self.point_type = ['noise'] * data.shape[0]

        # A list of clusters that each point belongs to -1 means no cluster
        self.clusters = np.full((data.shape[0], 1), -1)

        # take the first point, and compare it to all other points in the data
        for pointi, i in enumerate(data):

            # this is for keeping track of indices of points that are related
            # to pointi, but before we have enough relationships to designate it
            # a core point
            pre_core = []

            relate_counter = 0 #for keeping track of the number of relations

            cluster_counter = 0 #for naming new clusters

            for pointj, j in enumerate(data):

                # if at the same index, skip comparison (its the same point)
                if i == j:
                    continue

                # check to see if the points are within epsilon distance
                elif _distance(pointi, pointj) <= self.epsilon:
                    relate_counter += 1

                    # Check to see how many relations are made
                    # Track the less than min_samples relations
                    if relate_counter < self.min_samples:
                        pre_core.append(j)

                    # For exactly when you hit the min_samples and need to 
                    # upgrade pre_core points to be at least border
                    elif relate_counter == self.min_samples:
                        self.point_type[i] = 'core'

                        if self.clusters[i] >= 0:
                            cur_cluster = self.clusters[i]
                        else:
                            cur_cluster = cluster_counter
                            self.clusters[i] = cluster_counter

                        # realized this is moot, if a point is related to a core
                        # I will have already assigned it to that cluster
                        #
                        # for k in pre_core:
                        #     if self.point_type[k] == 'core':
                        #         # TODO, keep an eye on this, you may need to
                        #         # compare potential cur_clusters incase it 
                        #         # relates to multiple clusters. I suspect that
                        #         # will not be an issue though.
                        #         if self.clusters[k] < cur_cluster:
                        #             cur_cluster = self.clusters[k]
                        #     elif self.point_type[k] == 'border':
                        #         # TODO, keep an eye on this, I believe nothing
                        #         # should happen here, because two core points 
                        #         # could share a border point within epsilon
                        #         # distance, while that border point itself
                        #         # still hass fewer than min_samples meaning
                        #         # it would not impart the property of one 
                        #         # cluster onto another.
                        #         continue
                        
                        for k in pre_core:
                            if self.point_type[k] == 'noise':
                                self.point_type[k] = 'border'
                                self.clusters[k] = curr_cluster
                            else:

                                





    def cluster_ndimensional(self):
        pass # TODO: if I have time creat n-dimensional clustering