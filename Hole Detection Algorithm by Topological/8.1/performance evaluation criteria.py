# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 16:10:36 2020

@author: peter
"""
import numpy as np
import os

name = 'n=1000d=8'

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

def calAcc(orig_set, FD_set):
    allnode = list(range(1,1001))
    #read data
    orig_list = readData(orig_set)
    FD_list = readData(FD_set)
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
    with open(r'D:\result data\performance evaluation criteria\Sparse\FR\\' + name + '.txt','w') as f:
        #f.write("%s"%(holes_nodes[i][:]))
        f.write('TP:'+ str(TP))
        f.write(' TN:'+ str(TN))
        f.write(' FP:'+ str(FP))
        f.write(' FN:'+ str(FN))
        f.write(' Acc:' + str(acc))
        f.write(' Recall:' + str(recall))

    return acc, recall



def main():
    orig_set = os.path.abspath(r'D:\result data\dataset\Sparse\node id\\' + name + '.txt')
    FD_set = os.path.abspath(r'D:\result data\FD\Sparse\FR\\' + name + '\\node id\\' + name + '.txt')
    acc = calAcc(orig_set, FD_set)
    print('Acc:', acc)
    
if __name__ == "__main__":
    main()


