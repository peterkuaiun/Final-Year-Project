"""
Created on Tue Oct 22 18:09:16 2019

2019_UM_FST_CPS_FYP_Hole Detection in Sensor Network Project
FYP_22_10_2019
@author:     Ng Kim Hou
@Student ID: DB625369
@Description: 
1. Input the network data by using CNCAHNetGenerator
2. Using NetworkX Find all the node and edges
3. Draw back the network
4. Using OpenCV find the hole

   
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt

im = cv2.imread('data_5.png')
reults_img = im
imgray = cv2.cvtColor(reults_img,cv2.COLOR_BGR2GRAY)
_,binary = cv2.threshold(imgray,127,255,cv2.THRESH_BINARY_INV)
contours, hierarchy = cv2.findContours(binary,cv2.CHAIN_APPROX_NONE,cv2.CHAIN_APPROX_NONE)
area_min = 2000
area_mix = 50000
c_max = []
h, w, _ = im.shape
for i in range(len(contours)):
    cnt = contours[i]
    area = cv2.contourArea(cnt)
    if(area >= area_min and area <= area_mix):
        c_min = []
        c_min.append(cnt)
        cv2.drawContours(reults_img,c_min,-1,(200,200,100),-1)
        cv2.drawContours(reults_img,c_min,-1,(200,127,0),1)
        continue
    c_max.append(cnt)
print ("there are " + str(len(c_max)) + " contours")

plt.figure(num='Hole Detection in Sensor Network Project',
           figsize=(50,25),
           dpi=120)
img_1 = cv2.imread('data_5.png')
plt.subplot(121),plt.imshow(img_1),plt.title('Network'),plt.axis('off')
#plt.subplot(132),plt.imshow(imgray,'gray'),plt.title('IMGRAY Network'),plt.axis('off')
plt.subplot(122),plt.imshow(reults_img),plt.title('Result'),plt.axis('off')
plt.show()
print ("DONE.")