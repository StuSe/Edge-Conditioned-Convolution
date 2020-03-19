#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 14:35:27 2019

@author: Sebastian
"""


import os
import shutil as sh

#finds all OFF files and copies them into a folder

liste = []

# browse all subfolders for .off-files 
def find_off(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if os.path.join(root,name).endswith(".off"):
                # append an array with the paths of the .off-files
                liste.append(os.path.join(root,name))
                
    return liste
             
# "OFF_Files" is the name of the previously created folder where all files are copied to (has to be created in advance) 
for off_files in find_off("db"):
    sh.copy2(off_files, "OFF_Files")
   