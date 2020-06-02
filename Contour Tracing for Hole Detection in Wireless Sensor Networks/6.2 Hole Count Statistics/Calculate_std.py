# -*- coding: utf-8 -*-
import numpy as np
import sys
import os


path = str(sys.argv[1])
output_path = str(sys.argv[2])

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
folderlist = os.listdir(path)
for file in folderlist:
    fd_list = os.listdir(path + '\\' + file)
    for fd_name in fd_list:
        fd_result_txt = (path + '\\' + file + '\\' + fd_name)
        output_file_name = (output_path + '\\' + file + '\\' + fd_name)
        if not os.path.isdir(output_path + '\\' + file):
            os.mkdir(output_path + '\\' + file)
        num_hole = readData(fd_result_txt)
        standardDeviation(num_hole)
print('Done.')


