# DBSCAN algorithm
Density Based Spacial Clustering of Applications with Noise as written by myself.

A cluster is made by determining a points relationship to its neighboring points. So for each core point, there are minimum number of neighbors that make it a core point. If a corepoints neighbors are also corepoints, they are included in the cluster along with their neighbors. If a corepoints neighbors are not a corepoint (have less neighbors themselves), then it is a border point, included in the cluster but not it's neighbors. Any other points are noise.

## Definitions
*Point* = A singular data point. In 2 dimension space, think a single point on a cartesian graph.  

*Epsilon* = length of the radius from a point  

*Minimum Points* = the minimum number of points required to make a core point  

*Core Point* = A point with "minimum points" number of points within epsilon distance  

*Border Point* = A point belonging to a Core Point, that has less than the minimum number of points within epsilon distance  

*Noise point* = A point that doers not belong to a core point, and has less than the minimum number of points within epsilon distance  

*Cluster* = A group of points consisting of at least one Core point.  May or may not have border points.

## How would I do this
### First Pass
Assumptions, everything is noise until proven otherwise. Border points follow implicitly from core points.

A sequential solution
```
Compare point 1 and point 2
If within epsilon distance: 
    Add point 2 to point 1 relationship list, add point 1 to point 2s relationship list.

    If relationship list is greater than or equal to  minimum points:
        if point 1 is not core point:
            Set point 1 to a core point

        if point 1 belongs to a cluster:
            Set point 2 to belong to the same cluster
            Set point 2 to border point
        else:
            Set point 1 to a new cluster
            Set point 2 to the same cluster
            set point 2 to border point
```
So with this set up, if a point belongs to a cluster, but is not a core point, it is a border point by definition. If it is not a part of a cluster then it is noise by definition.

This solution is basically O(n^2) time complexity which is not awesome.  Wonder if I can get it down

It is O(n) space complexity, which is what ever, pretty much what I'd expect.

### Second Pass
The problem with my first pass, is I don't take into account how I'm traversing
my data.  If I compare each point sequentially, I could potentially run into
two points that are a part of the same cluster, but pretty far apart from each
other. And I would then treat them as though they are part of two different 
clusters.  This would just turn into a total mess with the right sized data. 
So instead I'm going to search until I find a core point, then I will iterate 
along its related points, until I've fully explored that cluster. Once that is 
done, I'll remove those explored points and traverse the remainder points, 
until I find the next core point.

```
Make a list of indices based off the passed in data.
Make a second empty list for your cluster relationships
a counter for cluster number

loop while length of indices list is greater than 0:

    Search for a core point
    Loop with point1 and compare to every other point in the indices list

        If within epsilon distance:
            Add point2 cluster relationships list

    Determine if core point is found
    if len relationship list >= min_samples:
        point1 is set to a core point
        point1 is set to cluster_counter group

        Explore entire cluster
        Determine if relationships are core or border points
        create a relationship subset list
        loop while over relationship list and compare each relationship to every point
            if within epsilon disatance:
                add pointB to relationship subset list
            
        if len subsetlist >= min_samples:
            pointA is set to a core point
            pointA is set to cluster_counter group
            find the points in subsetlist that are not in relationship list
            add to the end of relationship list
        else:
            pointA is a border point
            pointA is set to cluster_counter group
        
    Cluster is fully explored
    remove relationshiplist points from the indiceslist, because they have been fully explored and attributed to a cluster

    remove the point1 from the indices list

    increment cluster_counter

    restart loop if there are still indices left
```

This will keep the same time complexity of O(n^2). If the entire data set is noise, each point will get compared to each other in the list. If the data set is not entirely noise, then each point is compared to each other until a core point is found.  Then once a core point is found, each of those is compared to every point on the list.  Once the cluster is fully explored, those points are 'removed' and never checked against again.

Space complexity is n(cluster_list) + n(point types) + n(relationship_list). So O(3n) round to O(n) still.