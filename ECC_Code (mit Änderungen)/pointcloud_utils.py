#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 11:23:46 2019

@author: Sebastian
"""

from __future__ import division
from __future__ import print_function
from builtins import range

import random
import numpy as np
import math
import open3d
import igraph
from collections import defaultdict

RADIUS_MAX_K = 100 # maximum number of edges

def dropout(P,F,p):
    """ Removes points with probability p from vector of points and features"""
    idx = random.sample(range(P.shape[0]), int(math.ceil((1-p)*P.shape[0])))
    return P[idx,:], F[idx,:] if F is not None else None
    
def create_cloud(xyz, intensity=None, rgb=None):
    """ Creates Open3D point cloud from numpy matrices"""
    pcd = open3d.PointCloud()
    pcd.points = open3d.Vector3dVector(xyz)
    if intensity is not None:
        pcd.colors = open3d.Vector3dVector(np.tile(intensity, (1,3)))  # 1D intensity not supported
    elif rgb is not None:
        pcd.colors = open3d.Vector3dVector(rgb)
    return pcd
     
def create_graph(cloud, knn, radius, kd=None):
    """ Converts point cloud to graph by building neighborhood structure using kd-tree.
    Parameters:
    knn: true if using k-nn neighbors, false if using radius neighbors
    radius: radius if not knn, k if knn
    """
    xyz = np.asarray(cloud.points) # save points in array
    num_nodes = xyz.shape[0] # number of points

    kd = open3d.KDTreeFlann(cloud) if kd is None else kd
    idx, rowi = [], []  #includes self-loops
    if knn: # not relevant
        for i in range(len(cloud.points)):
            ind = kd.search_knn_vector_3d(cloud.points[i], int(radius))[1] # ind is an array with the indices of neighboring points for every point in the cloud
            idx.extend(ind); rowi.extend([i] * len(ind)) # idx contains all neighboring points; rowi contains the number of neighboring points, saved in the index of ind for later identification
    else:
        for i in range(len(cloud.points)):
            ind = kd.search_radius_vector_3d(cloud.points[i], radius)[1][:RADIUS_MAX_K]
            idx.extend(ind); rowi.extend([i] * len(ind))

    edges = np.vstack([idx, rowi]).T.tolist() # arrays with all pairs of neighboring points
    offsets = xyz[rowi] - xyz[idx] # distances between these points

    G = igraph.Graph(n=num_nodes, edges=edges, directed=True, edge_attrs={'offset':offsets}) 
    return G, kd         
    

def create_pooling_map(cloud_src, cloud_dst):
    """ Creates a pooling map from cloud_dst to cloud_src. Points in the denser cloud (source) are mapped to their nearest neighbor in the subsampled cloud (dest), thus no overlaps supported. """
    kd_dst = open3d.KDTreeFlann(cloud_dst)
    indices = [kd_dst.search_knn_vector_3d(cloud_src.points[i], 1)[1] for i in range(len(cloud_src.points))]
    
    poolmap = defaultdict(list)
    for si, di in enumerate(indices):
        poolmap[di[0]].append(si) 
    
    return poolmap, kd_dst
     
     
def create_graph_pyramid(args, cloud, pyramid_conf):
    """ Builds a pyramid of graphs and pooling operations corresponding to progressively coarsened point cloud using voxelgrid.
    Parameters:
    pyramid_conf: list of tuples (grid resolution, neigborhood radius/k), defines the pyramid
    """
    
    graphs = []
    pooldata = []
    prev_res = pyramid_conf[0][0] # assuming the caller performed the initial sampling.
    kd = None
    
    for res, rad in pyramid_conf:
        if prev_res != res:
            cloud_new = open3d.voxel_down_sample(cloud, voxel_size=res)
            poolmap, kd = create_pooling_map(cloud, cloud_new)
            cloud = cloud_new

        graph, kd = create_graph(cloud, args.pc_knn, rad, kd)    
        graphs.append(graph)   
        if prev_res != res:
            pooldata.append((poolmap, graphs[-2], graphs[-1]))
        prev_res = res

    return graphs, pooldata
