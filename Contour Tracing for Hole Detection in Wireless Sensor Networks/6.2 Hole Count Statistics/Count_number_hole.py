# -*- coding: utf-8 -*-
import numpy as np
import sys
import os

#dataset_txt = str(sys.argv[1])
fd_result_txt = str(sys.argv[1])
output_file = str(sys.argv[2])


#fd_result_txt = (r'D:\8.1. Result of Node Identifier Matching and Force-directed Algorithms\Result of peter_hole_detection_output_node_id\Sparse\\')


file_name_list = ['n=500d=6', 'n=500d=8', 'n=500d=10', 'n=500d=12', 'n=500d=15', 'n=1000d=6', 'n=1000d=8', 'n=1000d=10', 'n=1000d=12', 'n=1000d=15', 'n=2000d=6', 'n=2000d=8', 'n=2000d=10', 'n=2000d=12', 'n=2000d=15', 'n=3000d=6', 'n=3000d=8', 'n=3000d=10', 'n=3000d=12', 'n=3000d=15']

def readData(fname):
    hole = []
    data_f = open(fname)
    for line in data_f.readlines():
        nums = line.strip()
        hole.append(nums)
    num_hole = len(hole)
    num_hole = num_hole - 1
    
    return num_hole

def outputNumHole(fd_num_hole):
   with open(output_file_name + fd_name + '.txt','a') as f:
       f.write(str(fd_num_hole))
       f.write('\n')

#Main Program:
FD_name_list = os.listdir(fd_result_txt)
for file_name in file_name_list:
    for fd_name in FD_name_list:
        output_file_name = (output_file + '\\' + file_name + '\\')
        folderlist = os.listdir(fd_result_txt + '\\' + fd_name + '\\' + file_name + '\\')
        folderlist.sort(key= lambda x:int(x[:-4]))
        for fd_txt in folderlist:
            if not os.path.isdir(output_file_name):
                os.mkdir(output_file_name)
            fd_num_hole = readData(fd_result_txt + '\\' + fd_name + '\\' + file_name + '\\' + fd_txt)
            outputNumHole(fd_num_hole)
print('Done.')


