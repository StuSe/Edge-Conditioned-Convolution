#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 21:21:44 2019

@author: Sebastian
"""

import numpy as np
import open3d as op
import os

def main(main_path):
    
    i = 0
    # get the number of models in respective folders for later use in iterations
    for exfiles in os.walk(main_path):
        files = exfiles[2]
        anzahl_el = len(files)-1
        print(anzahl_el)        
    
    # iterate through all files for point cloud creation
    while i <= anzahl_el:
        path = main_path + "/" + files[i]
        
        x = path.split("/", 1)
        
        # address point cloud with points on vertices 
        pcvertices = op.read_point_cloud(path)
        # address point cloud with points on faces 
        pcsampling = op.read_point_cloud("ModelNetsPcd/modelnet10/" + x[1])
        
        # extract points from both point clouds
        points_vertices = np.asarray(pcvertices.points)
        points_sampling = np.asarray(pcsampling.points)
        # merge all points into one array 
        pcdmerged = np.vstack((points_sampling,points_vertices))
        
        
        point_cloud = op.PointCloud()
        point_cloud.points = op.Vector3dVector(pcdmerged)
        
        # write point cloud into folder structure 
        # modelnettest_merged: name of dataset has to be changed
        op.io.write_point_cloud('modelnettest_merged/' + x[1], point_cloud, write_ascii=True, compressed=False)
        
        i = i + 1
        
        
        
# initializes the process, the path must be changed for every class and test/train folder 
# the required datasets have to be located in the same folder
        
main('modelnettest/pc_sampled1k/chair/test')
