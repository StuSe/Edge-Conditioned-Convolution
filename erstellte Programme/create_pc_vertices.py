#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 14:24:36 2019

@author: Sebastian
"""

import numpy as np
import open3d as op
import trimesh 
import os
import sys
    
# creates point clouds with points on vertices of the CAD model
        
def main(main_path):
    
    i = 0
    # get the number of models in respective folders for later use in iterations
    for exfiles in os.walk(main_path):
        files = exfiles[2]
        count_el = len(files)-1
        print(count_el)        
   
    # iterate through all files for point cloud creation 
    while i <= count_el:
        x = files[i].split(".")
        path = main_path + "/" + files[i]
        
        points = np.asarray(read_off(path))
        point_cloud = op.PointCloud()
        point_cloud.points = op.Vector3dVector(points)
        #print(point_cloud)
        
        # write point cloud into folder structure (has to be created in advance)
        # modelnettest: name of dataset
        # toilet/test: must be changed for every path in main(...)
        op.io.write_point_cloud('modelnettest/pc_sampled1k/toilet/test/' + x[0] + ".pcd", point_cloud, write_ascii=True, compressed=False)
        
        i = i + 1       




        
def read_off(file): # (inspired by: https://davidstutz.de/visualizing-triangular-meshes-from-off-files-using-python-occmodel/)
 
    assert os.path.exists(file)
 
    with open(file, 'r') as fp:
        lines = fp.readlines()
        lines = [line.strip() for line in lines]
 
        assert lines[0] == 'OFF'
 
        splitted = lines[1].split(' ')
        assert len(splitted) == 3
 
        count_vertices = int(splitted[0])
        assert count_vertices > 0
 
        count_faces = int(splitted[1])
        assert count_faces > 0
 
        vertices = []
        for i in range(count_vertices):
            vertex = lines[2 + i].split(' ')
            vertex = [float(point) for point in vertex]
            assert len(vertex) == 3
 
            vertices.append(vertex)
 
        faces = []
        for i in range(count_faces):
            face = lines[2 + count_vertices + i].split(' ')
            face = [int(index) for index in face]
 
            assert face[0] == len(face) - 1
            for index in face:
                assert index >= 0 and index < count_vertices
 
            assert len(face) > 1
 
            faces.append(face)
 
        return vertices
        

# initializes the process, the path must be changed for every class and test/train folder      
main('ModelNet10/toilet/test')