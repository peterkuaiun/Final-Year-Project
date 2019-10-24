"""
Created on Thu Oct 24 00:29:03 2019

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

img = cv2.imread('data_5.png')
reults_img = img.copy()
area_min = 1000
area_mix = 50000
c_max = []
#h, w, _ = img.shape

imgray = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY)
_,binary = cv2.threshold(imgray.copy(),254,255,3)
contours,_ = cv2.findContours(binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
print ("there are " + str(len(contours)) + " contours")
mask = np.zeros(imgray.shape, dtype='uint8')
for i in range(len(contours)):
    area = cv2.contourArea(contours[i])
    if(area >= area_min and area <= area_mix):
        c_min = []
        c_min.append(contours[i])
        cv2.drawContours(reults_img,c_min,-1,(200,200,100),-1),cv2.drawContours(reults_img,c_min,-1,(200,127,0),1)
        cv2.drawContours(mask,c_min, -1, 255, -1)
        continue
    c_max.append(contours[i])
print ("there are " + str(len(c_max)) + " contours in C_max")

plt.figure(num='Hole Detection in Sensor Network Project',
           figsize=(50,25),
           dpi=120)
plt.subplot(231),plt.imshow(img),plt.title('Network'),plt.axis('off')
plt.subplot(232),plt.imshow(reults_img),plt.title('Result'),plt.axis('off')
plt.subplot(233),plt.imshow(cv2.bitwise_and(img, img, mask=mask)),plt.title('MASK'),plt.axis('off')
plt.subplot(234),plt.imshow(binary,'gray'),plt.title('binary'),plt.axis('off')
plt.subplot(235),plt.imshow(imgray,'gray'),plt.title('imgray'),plt.axis('off')
plt.show()
print ("DONE.")