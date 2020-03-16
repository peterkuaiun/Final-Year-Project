# -*- coding: utf-8 -*-
import numpy as np
import sys
import os


#dataset_txt = str(sys.argv[1])
#fd_result_txt = str(sys.argv[2])
#output_file_name = str(sys.argv[3])

def readData(fname):
    num_hole = []
    data_f = open(fname)
    for line in data_f.readlines():
        nums = line.strip()
        num_hole.append(int(nums))
    
    return num_hole

def standardDeviation(num_hole):
    std_value = np.std(num_hole, ddof=1)
    mean_value = np.mean(num_hole)
    max_value = max(num_hole)
    min_value = min(num_hole)
   
    with open(output_file_name,'w') as f:
       f.write(str(std_value))
       f.write(',')
       f.write(str(mean_value))
       f.write(',')
       f.write(str(max_value))
       f.write(',')
       f.write(str(min_value))
       f.write('\n')

#Main Program:
path = (r'D:\8.2. Result of Number Of Hole Matching\Sparse\Each FD number of hole\\')
folderlist = os.listdir(path)
for file in folderlist:
    fd_list = os.listdir(path + file)
    for fd_name in fd_list:
        fd_result_txt = (path + file + '\\' + fd_name)
        output_path = (r'D:\8.2. Result of Number Of Hole Matching\Sparse\Result of STD Calculation\\')
        output_file_name = (output_path + file + '\\' + fd_name)
        if not os.path.isdir(output_path + file):
            os.mkdir(output_path + file)
        num_hole = readData(fd_result_txt)
        standardDeviation(num_hole)
        print('Finish ' + output_path + file)
print('Done.')


