"""
Created on Tue Jun  2 22:05:20 2020

@author:     Ng Kim Hou
@Student ID: DB625369
@Description:
    -The Hole Detection in sensor network by CNN.
    -This code output compared performance of CTA & CNN
    
"""
import numpy as np
import os

def readData(fname):
    print("[LOADING]:%s"%fname)
    data_list = []
    data_f = open(fname)
    for line in data_f.readlines():
        nums = line.strip().split(',')
        nums = [item.replace('[', '').replace(']', '').replace(' ', '') for item in nums]
        if nums[0] == 'NULL' or nums[0] == ' ':
            print("[INFO]: NULL HOLE",nums)
            nums = []
        else:
            nums = [int(x) for x in nums]
            matrix = np.array(nums)
            matrix = matrix.transpose()
            MatToList = matrix.tolist()
            for i in range(len(MatToList)):
                #print(MatToList[i])
                data_list.append(MatToList[i])
    return data_list 

def calAcc(orig_list, FD_list,output_file_name): 
    num_nodes = int(orig_list.pop(0))
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
    if (TP+FN == 0):
        sensitivity = 0
        specificity = 0
    else:
        sensitivity = TP / (TP + FN)
        specificity = TN / (TN + FP)
    #print('TP:', TP,' TN:', TN, ' FP:', FP, ' FN:',FN)
    with open(output_file_name,'w') as f:
        #f.write("%s"%(holes_nodes[i][:]))
        f.write('TP:'+ str(TP))
        f.write(' TN:'+ str(TN))
        f.write(' FP:'+ str(FP))
        f.write(' FN:'+ str(FN))
        f.write(' Sensitivity:' + str(sensitivity))
        f.write(' Specificity:' + str(specificity))
        print('[INFO] TP:%d TN:%d FP:%d FN:%d Sensitivity:%d Specificity:%d \n' %(TP,TN,FP,FN,sensitivity,specificity))
        
    return sensitivity, specificity

#Main Program:
#input the detected hole node file.
path = input("Input the 2 path of detected hole node in sensor network and the result output path:")
path  = path.split()

'''
path_1 = 'fd-CTA/Sparse/DH/' #The data file name
path_2 = 'fd-YOLO/Sparse/DH/' #The data file name
path_reult_txt = 'result/FD-CTA_FD-YOLO_result/Sparse/DH/'
'''
if len(path)==3: 
    path_1 = path[0]
    path_2 = path[1]
    path_reult_txt = path[2]
    
    if not os.path.exists(path_reult_txt):
        os.makedirs(path_reult_txt)
    dataset_txt_1 = ' '
    dataset_txt_2 = ' '
    dirs_1 = []
    dirs_1 = os.listdir(path_1)
    dirs_2 = []
    dirs_2 = os.listdir(path_2)
     
    for i in range(0,len(dirs_1)):
        dataset_txt_1 = path_1 + dirs_1[i]
        dataset_txt_2 = path_2 + dirs_2[i]
        dt1_name = os.path.basename(dirs_1[i]).split('_')[0]
        dt2_name = os.path.basename(dirs_1[i]).split('_')[0]
        if dt1_name == dt2_name:
                base = dt1_name+'.txt'
                output_file_name = path_reult_txt+base
                dataset_1 = readData(dataset_txt_1)
                dataset_2 = readData(dataset_txt_2)
                calAcc(dataset_1, dataset_2,output_file_name)
    print('[DONE] ALL DONE')
else:
    print('[ERORR] WRONG INPUT!!!')



