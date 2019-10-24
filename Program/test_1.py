"""
Created on Mon Oct  7 22:51:38 2019

@author:     Ng Kim Hou
@Student ID: DB625369
@Description:
    
"""
import cv2 
import numpy as np 

img = cv2.imread('test_1.png') 
lowerb = np.array([0, 0, 0]) 
upperb = np.array([254, 254, 254]) 
red_line = cv2.inRange(img, lowerb, upperb) 

cv2.imshow('red', red_line)
cv2.waitKey(0) 
