"""
Created on Thu Oct 10 17:29:07 2019

@author:     Ng Kim Hou
@Student ID: DB625369
@Description:
    
"""

import numpy as np
import cv2

im = cv2.imread('data_5.png')
#cv2.imshow('network', im)
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
#cv2.imshow('network', imgray)
_,binary = cv2.threshold(imgray,127,255,cv2.THRESH_BINARY_INV)
cv2.imshow('network', binary)
contours, hierarchy = cv2.findContours(binary,cv2.CHAIN_APPROX_NONE,cv2.CHAIN_APPROX_NONE)
print ("there are " + str(len(contours)) + " contours")
for i in range(1,len(contours)-1):
    ellipse = cv2.fitEllipse(contours[i])
    img = cv2.ellipse(img,ellipse,(0,255,0),2)
    #approx = cv2.approxPolyDP(contours[i],0.5,True)
    cv2.drawContours(im,[approx],-1,(200,200,100),-1)

cv2.imshow('result network', im)
cv2.waitKey(0)
cv2.destroyAllWindows()