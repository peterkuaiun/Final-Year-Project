# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 01:59:13 2020

@author: peter
"""
import pandas as pd
import os

file_name = ['n=500d=6', 'n=500d=8', 'n=500d=8', 'n=500d=10', 'n=500d=12', 'n=500d=15', 'n=1000d=6', 'n=1000d=8', 'n=1000d=10', 'n=1000d=12', 'n=1000d=15', 'n=2000d=6', 'n=2000d=8', 'n=2000d=10', 'n=2000d=12', 'n=2000d=15', 'n=3000d=6', 'n=3000d=8', 'n=3000d=10', 'n=3000d=12', 'n=3000d=15']
FD_path = []
df_FD = []
path = (r'D:\8.2. Result of Number Of Hole Matching\Sparse\Result of STD Calculation\n=3000d=15\\')
FD_list = os.listdir(path)
for FD_name in FD_list:
    FD_path.append(path + FD_name)
    
output = (path + 'result_table.csv')

df_FD = pd.read_csv(FD_path[0], sep=",", header=None)
#df_FA2 = pd.read_csv(FD_path[1], sep=",", header=None)
FD_path.pop(0)

for index in FD_path:
    df_FD = df_FD.append(pd.read_csv(index, sep=",", header=None))
df_FD.reset_index(drop=True, inplace=True)
    
FD_name = ['DH', 'FA2', 'FDGE', 'FR', 'FRR', 'FRU', 'JIGGLE', 'KK', 'KK-MS-DS', 'LINLOG']
df_FD_name = pd.DataFrame(FD_name)
df_result = pd.concat([df_FD_name, df_FD], axis=1)
df_result.columns = ['Force-Direct Algorithms', 'Standard Deviation', 'Mean', 'Maximun', 'Minimun']
#df_FD.rename(columns={0:'Standard Deviation', 1:'Mean', 2:'Maximun', 3:'Minimun'}, inplace=True)
#df_FD.rename(columns={0:'Standard Deviation', 1:'Mean', 2:'Maximun', 3:'Minimun'}, index=['DH', 'FA2', 'FDGE', 'FR', 'FRR', 'FRU', 'JIGGLE', 'KK', 'KK-MS-DS', 'LINLOG'], inplace=True)

df_result.to_csv(output, sep= ',', index=False)
print('Done.')