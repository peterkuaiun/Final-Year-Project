"""
Created on Mon Oct  7 00:21:49 2019
2019_UM_FST_CPS_FYP_Hole Detection in Sensor Network Project

FYP_07_10_2019
@author:     Ng Kim Hou
@Student ID: DB625369
@Description: 
1. Test input an image convert to bitmap
2. Find all the edges 
   
"""
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np

#Input the image and the image convert RGB mode 
img = Image.open("test_1.png").convert('RGB')

#Copy the image
b_img = img.copy()

#load the image
pixels = b_img.load()

'''

#useing the black pixels to find the edges 
for x in range(b_img.height-1):
    for y in range(b_img.width-1):
        
        #If the pixels is black, change the color to red.
        if (pixels[x, y] != (255, 255, 255)):
            pixels[x, y] = (255, 0, 0)
'''

         
img2 = cv2.imread('test_1.png')
p_list = []
lowerb = np.array([0, 0, 0]) 
upperb = np.array([254, 254, 254])
network = cv2.inRange(img2, lowerb, upperb)
t_point = np.zeros((network.shape[0],network.shape[1]))
cv2.imshow('network',network)
cv2.waitKey(0)
def find_point(img,x,y):
    if (x >= img.shape[0] -4 or y >= img.shape[1] - 4):
        return False
    #print('img:',img_a)
    #print('x:',x_1)
    #print('y:',y_1)
    for x_1 in range(x,x+4):
        #print('x:',x_1)
        for y_1 in range(y,y+4):
            #print('y:',y_1)
            if (img[x,y] == 0):
                #print('not a point:',img_a[x_1,y_1],x_1,y_1)
                return False
    return True

for x in range(network.shape[0]-4):
    for y in range(network.shape[1]-4):        
        #If the pixels is black, change the color to red.
        
        if (find_point(network,x,y) == True):
             p_list.append([x+3,y+3])
             t_point[x+3,y+3] = 255
             x= x+3
             y= y+3





        




cv2.imshow('Point',t_point)
cv2.waitKey(0) 
print('DONE')
'''
#Save the image as bitmap
b_img.save("test1.bmp")

plt.figure("img")
plt.imshow(img)
plt.figure("b_img")
plt.imshow(b_img)

plt.title('the result')
plt.show()
'''
