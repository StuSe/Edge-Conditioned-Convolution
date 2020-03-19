#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 16:27:59 2019

@author: Sebastian
"""
import trimesh
import numpy as np
import open3d as op


#READS THE TEXTFILE, OPENS THE CORRESPONDING OFF FILES AND SAVES THEM AS .pcd

def sample_pc(mesh, points): # (inspired by: https://github.com/mikedh/trimesh/blob/master/trimesh/sample.py)
    
    area = mesh.area_faces
    
    # total area (float)
    sum_area = np.sum(area)
    # cumulative area
    cum_area = np.cumsum(area)
    
    # generates random points between 0 and 1 and multiplies them for insertion puposes 
    random_points = np.random.random(points) * sum_area
    face_id = np.searchsorted(cum_area, random_points)
    
    # transform faces in the sense of analytical geometry
    sup_vec = mesh.triangles[:, 0] #one point of the triangle
    di_vec = mesh.triangles[:, 1:].copy() #other two points of the triangle
    di_vec -= np.tile(sup_vec, (1, 2)).reshape((-1, 2, 3)) # vectors with sup_vec as origin
    
    
    # get face id
    sup_vec = sup_vec[face_id]
    di_vec = di_vec[face_id]

    # generate random numbers between 0 and 1 
    scalar_comp = np.random.random((len(di_vec), 2, 1))
    # points are sampled in a square when the value of the sum of the two numbers is greater then 1
    # goal: find values > 1 and transform them for fitting in the triangle (<1)
    random_test = scalar_comp.sum(axis=1).reshape(-1) > 1.0
    scalar_comp[random_test] -= 1.0
    print(scalar_comp)
    scalar_comp = np.abs(scalar_comp)
    # multiply numbers with direction vectors and sum the resulting vectors
    sample_vector = (di_vec * scalar_comp).sum(axis=1)
    
    #add the support vektor
    points = sample_vector + sup_vec

    return points


array = []

def off2pc_merged(path):
    i = 0
    # get the files
    with open(path, "r") as file:
        x = file.read().splitlines()
        print(x)
    
    # run through all files 
    while i < len(x):
        filename = x[i]
        #load OFF-file
        mesh = trimesh.load('OFF_Files/m' + filename + '.off')
        # generate points on surfaces and points on edges
        points = np.asarray(mesh.vertices)
        points_sampled = np.asarray(sample_pc(mesh, 1000))
        # merge points of two point clouds
        points_merged = np.vstack((points_sampled,points))
        point_cloud = op.PointCloud()
        point_cloud.points = op.Vector3dVector(points_merged)
        
        #save the resulting point cloud
        op.io.write_point_cloud('classification/v1/benchmark_files_test/animal/test/animal_' + filename +'.pcd', point_cloud, write_ascii=True, compressed=False)
    
        i = i + 1
        
    return x          

# "vehicle/train/vehicle.txt" has to be changed for every class and train/test split 
#off2pc_merged("classification/v1/benchmark_files_test/animal/test/animal.txt")
    
    
def off2pc_vertices(path):
    i = 0
    
    with open(path, "r") as file:
        x = file.read().splitlines()
        print(x)
    
    
    while i < len(x):
        filename = x[i]
        #load OFF-file
        mesh = trimesh.load('OFF_Files/m' + filename + '.off')
        points = np.asarray(mesh.vertices)
        point_cloud = op.PointCloud()
        point_cloud.points = op.Vector3dVector(points)
        
        # has to be changed:
        # initial folder where the data is located ("benchmark_files_vertices")
        # class ("vehicle")
        # "train" or "test"
        # name of the file ("vehicle_")
        op.io.write_point_cloud('classification/v1/benchmark_files_vertices/vehicle/train/vehicle_' + filename +'.pcd', point_cloud, write_ascii=True, compressed=False)
    
        i = i + 1
        
    return x

# "vehicle/train/vehicle.txt" has to be changed for every class and train/test split
#off2pc_vertices("classification/v1/benchmark_files_vertices/vehicle/train/vehicle.txt")  
    

def off2pc_sampling(path):
    i = 0
    
    with open(path, "r") as file:
        x = file.read().splitlines()
        print(x)
    
    
    while i < len(x):
        filename = x[i]
        #load OFF-file
        mesh = trimesh.load('OFF_Files/m' + filename + '.off')
        # sample points
        points_sampled = np.asarray(sample_pc(mesh, 1000))
        # create point cloud object
        point_cloud = op.PointCloud()
        point_cloud.points = op.Vector3dVector(points_sampled)
        
        #save the resulting point cloud
        
        # has to be changed: 
        # initial folder where the data is located ("benchmark_files_sampled")
        # class ("vehicle")
        # "train" or "test"
        # name of the file ("vehicle_")
        op.io.write_point_cloud('classification/v1/benchmark_files_sampled/vehicle/train/vehicle_' + filename +'.pcd', point_cloud, write_ascii=True, compressed=False)
    
        i = i + 1
        
    return x


def mean_and_covariance(pointcloud):
    mesh = trimesh.load(pointcloud)
    points_sampled = np.asarray(sample_pc(mesh, 1000))
    point_cloud = op.PointCloud()
    point_cloud.points = op.Vector3dVector(points_sampled)
    print(op.geometry.compute_point_cloud_mean_and_covariance(point_cloud))


# "vehicle/train/vehicle.txt" has to be changed for every class and train/test split
#off2pc_sampling("classification/v1/ECC_txt_Vorlage/vehicle/train/vehicle.txt")
    










