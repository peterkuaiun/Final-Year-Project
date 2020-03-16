# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 01:59:13 2020

@author: peter
"""
import pandas as pd
import os

file_name = ['n=500d=6', 'n=500d=8', 'n=500d=8', 'n=500d=10', 'n=500d=12', 'n=500d=15', 'n=1000d=6', 'n=1000d=8', 'n=1000d=10', 'n=1000d=12', 'n=1000d=15', 'n=2000d=6', 'n=2000d=8', 'n=2000d=10', 'n=2000d=12', 'n=2000d=15', 'n=3000d=6', 'n=3000d=8', 'n=3000d=10', 'n=3000d=12', 'n=3000d=15']

FD_name_list = os.listdir(r'D:\8.1. Result of Node Identifier Matching and Force-directed Algorithms\Result of peter_hole_detection_output_node_id\Sparse\\')
for index in file_name:
    for fd_name in FD_name_list:
        FD_data = (r'D:\result_data\test\hole\\' + index + '\\'+ fd_name +'.txt')
        csv_data = (r'D:\8.1. Result of Node Identifier Matching and Force-directed Algorithms\Uniform\\' + fd_name + '\\' + index + '.csv')
        output = (r'D:\result_data\test\result\\' + index + '\\' + fd_name + '.txt')
        if not os.path.isdir(r'D:\result_data\test\result\\' + index):
            os.mkdir(r'D:\result_data\test\result\\' + index)
        df_FD = pd.read_csv(FD_data, sep=" ", header=None)
        df_csv = pd.read_csv(csv_data, sep=",", usecols=[0], skiprows=1, header=None)
        df_csv[1] = df_FD[0]
        df_csv.to_csv(output, sep= ' ', index=False)
        print('finish ' + index + fd_name)
print('Done.')