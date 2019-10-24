"""
Created on Thu Oct 24 00:29:03 2019

@author:     Ng Kim Hou
@Student ID: DB625369
@Description:


2019_UM_FST_CPS_FYP_Hole Detection in Sensor Network Project
FYP_24_10_2019
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

img = np.zeros((1080, 1080, 3), np.uint8) #create a gray img
img_1 = cv2.imread('data_5.png')
reults_img = img.copy()
area_min = 1000
area_mix = 50000
c_max = []
print (img.shape)


fname = 'data_5' #The data file name
out_format = '.png' #The output image format
data_list = [] #The data list

#The node and edge attributes
num_nodes = int
all_nodes = []
num_edges = int
all_edges = []

#Create the data list
data_f = open(fname, 'r')
for line in data_f.readlines():
    data_list.append(line.strip())
data_f.close

num_nodes = int (data_list.pop(0)) #Pop out the number of nodes 

#Get all the number node coordinate
for i in range (0,num_nodes):
    node = data_list.pop(0) #Pop out the node coordinate
    node = node.split()
    node.pop(0) #Pop out the node index  
    all_nodes.append((int(float (node[0])*1000.0),int(float (node[1])*1000.0))) #(X, Y)  
num_edges = int (data_list.pop(0)) #Pop out the number of edges 

#Get all the edge
for i in range (0,num_edges): 
    edge = data_list.pop(0) #Pop out the edge connection
    edge = edge.split()
    all_edges.append([int(edge[0]),int(edge[1])]) #(point 1, point 2)

#Add all the edges    
for i in range (0,num_edges): 
    cv2.line(img, all_nodes[all_edges[i][0]], all_nodes[all_edges[i][1]], (252, 121, 120), 3)  #Add the edge connection
    

#np.transpose(img)
reults_img = img.copy()
area_min = 4000
area_mix = 50000
c_max = []
#h, w, _ = img.shape

imgray = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY)
_,binary = cv2.threshold(imgray.copy(),254,255,2)
contours,_ = cv2.findContours(binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
print ("there are " + str(len(contours)) + " contours")
mask = np.zeros(imgray.shape, dtype='uint8')

#Find the hole in the network
for i in range(len(contours)):
    area = cv2.contourArea(contours[i])
    if(area >= area_min and area < area_mix):
        c_min = []
        c_min.append(contours[i])
        cv2.drawContours(reults_img,c_min,-1,(246,235,123),-1)
        cv2.drawContours(reults_img,c_min,-1,(194,232,206),1)
        cv2.drawContours(mask,c_min, -1, 255, -1)
        c_max.append(contours[i])
        continue
        

#Add all the nodes
for i in range (0,num_nodes): 
    cv2.circle(reults_img, all_nodes[i], 3,(94,183,183), -1, 0, 0)  #Add the node result
    cv2.circle(img, all_nodes[i], 3,(94,183,183), -1, 0, 0)  #Add the node network


print ("there are " + str(len(c_max)) + " contours in C_max")

plt.figure(num='Hole Detection in Sensor Network Project',
           figsize=(50,25),
           dpi=200)
plt.imshow(img),plt.title('Network'),plt.axis('off')
plt.subplot(231),plt.imshow(img_1),plt.title('Network'),plt.axis('off')
plt.subplot(232),plt.imshow(img),plt.title('DRAW_NETWORK'),plt.axis('off')
plt.subplot(233),plt.imshow(cv2.bitwise_and(reults_img, reults_img, mask=mask)),plt.title('MASK'),plt.axis('off')
plt.subplot(234),plt.imshow(reults_img),plt.title('reults_IMG'),plt.axis('off')
plt.subplot(235),plt.imshow(imgray,'gray'),plt.title('imgray'),plt.axis('off')
plt.show()
print ("DONE.")