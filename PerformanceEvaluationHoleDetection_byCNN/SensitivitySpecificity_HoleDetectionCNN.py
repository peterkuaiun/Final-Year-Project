"""
Created on Tue Jun  2 22:05:20 2020

@author:     Ng Kim Hou
@Student ID: DB625369
@Description:
    -The Hole Detection in sensor network by CNN.
    -This code will output compared performance result for GNUplot
    
"""
import os
import pandas as pd

def readData(fname):
    n = os.path.basename(fname).split('n=')[1].split('d=')[0]
    d = os.path.basename(fname).split('d=')[1].split('.')[0]
    d = d.split('_')[0]

    with open(fname,'r') as f:
        data = f.read().split(' ')
    data[0] = data[0].split('TP:')[1]
    data[1] = data[1].split('TN:')[1]
    data[2] = data[2].split('FP:')[1]
    data[3] = data[3].split('FN:')[1]
    data[4] = data[4].split('Sensitivity:')[1]
    data[5] = data[5].split('Specificity:')[1]
    
    dic = {"n": int(n), 
           "d": int(d),
           "TP": float(data[0]),
           "TN": float(data[1]),
           "FP": float(data[2]),
           "FN": float(data[3]),
           "Sensitivity":float(data[4]),
           "Specificity": float(data[5])}
    return dic


def convertDF(path= " " ,dirs = []):
    df = pd.DataFrame(columns = ["n", "d","TP","TN","FP","FN","Sensitivity","Specificity"])
    for i in range(len(dirs)):
        data = readData(path + dirs[i])
        df = df.append(data,ignore_index=True)
    df = df.sort_values(by=['n','d'])
    df.reset_index(inplace=True)
    df = df.drop(labels=["index"], axis="columns")
    return df

def cul_avg_d(df):

    df_d6 = df[df["d"]==6]
    df_d8 = df[df["d"]==8]
    df_d10 = df[df["d"]==10]
    df_d12 = df[df["d"]==12]
    df_d15 = df[df["d"]==15]

    df_spc = pd.Series(index = [6,8,10,12,15])
    
    df_spc[6] = str(int(df_d6['Specificity'].mean() * 100))+'%'
    df_spc[8] = str(int(df_d8['Specificity'].mean() * 100))+'%'
    df_spc[10] = str(int(df_d10['Specificity'].mean() * 100))+'%'
    df_spc[12] = str(int(df_d12['Specificity'].mean() * 100))+'%'
    df_spc[15] = str(int(df_d15['Specificity'].mean() * 100))+'%'

    df_tpr = pd.Series(index = [6,8,10,12,15])
    
    df_tpr[6] = str(int(df_d6['Sensitivity'].mean() * 100))+'%'
    df_tpr[8] = str(int(df_d8['Sensitivity'].mean() * 100))+'%'
    df_tpr[10] = str(int(df_d10['Sensitivity'].mean() * 100))+'%'
    df_tpr[12] = str(int(df_d12['Sensitivity'].mean() * 100))+'%'
    df_tpr[15] = str(int(df_d15['Sensitivity'].mean() * 100))+'%'
    
    return df_spc,df_tpr

def cul_avg_n(df):

    df_n500 = df[df["n"]==500]
    df_n1000 = df[df["n"]==1000]
    df_n2000 = df[df["n"]==2000]
    df_n3000 = df[df["n"]==3000]

    df_spc = pd.Series(index = [500,1000,2000,3000])
    
    df_spc[500] = str(int(df_n500['Specificity'].mean() * 100))+'%'
    df_spc[1000] = str(int(df_n1000['Specificity'].mean() * 100))+'%'
    df_spc[2000] = str(int(df_n2000['Specificity'].mean() * 100))+'%'
    df_spc[3000] = str(int(df_n3000['Specificity'].mean() * 100))+'%'

    df_tpr = pd.Series(index = [500,1000,2000,3000])
    
    df_tpr[500] = str(int(df_n500['Sensitivity'].mean() * 100))+'%'
    df_tpr[1000] = str(int(df_n1000['Sensitivity'].mean() * 100))+'%'
    df_tpr[2000] = str(int(df_n2000['Sensitivity'].mean() * 100))+'%'
    df_tpr[3000] = str(int(df_n3000['Sensitivity'].mean() * 100))+'%'

    
    return df_spc,df_tpr
    
    
def cul_all(path,result_path):
    path_1 = os.listdir(path)
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    for i in path_1:
        print('[LOADING]%s' %i)       
        dirs = []
        dirs = os.listdir(path + i)
            
        SPCd_txt = '%s/%s-SPC-By-avg.txt' %(result_path,i)
        TPRd_txt = '%s/%s-TPR-By-avg.txt' %(result_path,i)
        SPCn_txt = '%s/%s-SPC-By-node.txt' %(result_path,i)
        TPRn_txt = '%s/%s-TPR-By-node.txt' %(result_path,i)
        
        
        df=convertDF(path + i + '/' ,dirs)
        df_SPCd,df_TPRd = cul_avg_d(df)
        df_SPCd.to_csv(SPCd_txt, sep='\t', index=True)
        df_TPRd.to_csv(TPRd_txt, sep='\t', index=True)
        
        df_SPCn,df_TPRn = cul_avg_n(df)

        df_SPCn.to_csv(SPCn_txt, sep='\t', index=True)
        df_TPRn.to_csv(TPRn_txt, sep='\t', index=True)
        
        print('[DONE] %s done.\n' %i)

    
'''
#GT-CTA_GT-YOLO_result
s_path = 'result/GT-CTA_GT-YOLO_result/Sparse/' #The path of compared performance result
s_result_path = 'GNUPlot/txt-result/GT-CTA_GT-YOLO_result/Sparse/' #The path for saved the result
u_path = 'result/GT-CTA_GT-YOLO_result/Uniform/' #The path of compared performance result
u_result_path = 'GNUPlot/txt-result/GT-CTA_GT-YOLO_result/Uniform/' #The path for saved the result
cul_all(s_path,s_result_path)
cul_all(u_path,u_result_path)
print('[DONE] ALL DONE.')

#GT-CTA_FD-YOLO_result
s_path = 'result/GT-CTA_FD-YOLO_result/Sparse/' #The path of compared performance result
s_result_path = 'GNUPlot/txt-result/GT-CTA_FD-YOLO_result/Sparse/' #The path for saved the result
u_path = 'result/GT-CTA_FD-YOLO_result/Uniform/' #The path of compared performance result
u_result_path = 'GNUPlot/txt-result/GT-CTA_FD-YOLO_result/Uniform/' #The path for saved the result
cul_all(s_path,s_result_path)
cul_all(u_path,u_result_path)
print('[DONE] ALL DONE.')

#FD-CTA_FD-YOLO_result
s_path = 'result/FD-CTA_FD-YOLO_result/Sparse/' #The path of compared performance result
s_result_path = 'GNUPlot/txt-result/FD-CTA_FD-YOLO_result/Sparse/' #The path for saved the result
u_path = 'result/FD-CTA_FD-YOLO_result/Uniform/' #The path of compared performance result
u_result_path = 'GNUPlot/txt-result/FD-CTA_FD-YOLO_result/Uniform/' #The path for saved the result
cul_all(s_path,s_result_path)
cul_all(u_path,u_result_path)
print('[DONE] ALL DONE.')
'''

path = input("Input the path of performance result in sensor network and the result output path:")
path  = path.split()
cul_all(path[0],path[1])
print('[DONE] ALL DONE.')



