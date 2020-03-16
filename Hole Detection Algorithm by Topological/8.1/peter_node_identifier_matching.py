# -*- coding: utf-8 -*-
import numpy as np
import sys

dataset_txt = str(sys.argv[1])
fd_result_txt = str(sys.argv[2])
output_file_name = str(sys.argv[3])

def readData(fname):
    data_list = []
    data_f = open(fname)
    for line in data_f.readlines():
        nums = line.strip().split(',')
        nums = [item.replace('[', '').replace(']', '').replace(' ', '') for item in nums]
        nums = [int(x) for x in nums]
        matrix = np.array(nums)
        matrix = matrix.transpose()
        MatToList = matrix.tolist()
        for i in range(len(MatToList)):
            #print(MatToList[i])
            data_list.append(MatToList[i])
    return data_list

def calAcc(orig_list, FD_list):
    num_nodes = int(dataset.pop(0))
    FD_list.pop(0)
    
    allnode = list(range(1, num_nodes+1))
    #calulate TP and TN, find the duplicate node id will get TP
    t_intersection = list(set(orig_list).intersection(set(FD_list)))
    TP = len(t_intersection)
    FP = len(orig_list) - TP
    #find the difference node id between the node in the hole and all node, will get the the node id out of the hole
    orig_list_outside = list(set(orig_list).symmetric_difference(set(allnode)))
    FD_list_outside = list(set(FD_list).symmetric_difference(set(allnode)))
    #calulate FP and FN, find the duplicate node id will get FP
    n_intersection = list(set(orig_list_outside).intersection(set(FD_list_outside)))
    TN = len(n_intersection)
    FN = len(FD_list_outside) - TN
    #confusion matrix accuracy formula
    acc = (TP + TN) / (TP + TN + FP + FN)
    recall = TP / (TP + FN)
    #print('TP:', TP,' TN:', TN, ' FP:', FP, ' FN:',FN)
    with open(output_file_name,'w') as f:
        #f.write("%s"%(holes_nodes[i][:]))
        f.write('TP:'+ str(TP))
        f.write(' TN:'+ str(TN))
        f.write(' FP:'+ str(FP))
        f.write(' FN:'+ str(FN))
        f.write(' Acc:' + str(acc))
        f.write(' Recall:' + str(recall))

    return acc, recall

#Main Program:
dataset = readData(dataset_txt)
fd_result = readData(fd_result_txt)
calAcc(dataset, fd_result)



