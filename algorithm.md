# DBSCAN algorithm
Density Based Spacial Clustering of Applications with Noise as written by myself.

This is a first pass to verify if I understand the concept, before relying on another more professionally written algorithm.

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