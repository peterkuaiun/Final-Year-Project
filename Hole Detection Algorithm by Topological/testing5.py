# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:04:11 2020

@author: peter
"""
import os

g = (r'D:\data\result\\')
for root, dirs, files in os.walk('g'):
    for dir in dirs:
        print(os.path.join(root, dir))