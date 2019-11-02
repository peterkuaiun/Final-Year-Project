"""
Created on Thu Oct 31 15:27:02 2019

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
area_holes = []

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
    

reults_img = img.copy()
area_min = 4000
area_mix = 50000
area_holes = []

#Create the gray Image for Image Processing
imgray = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY)
_,binary = cv2.threshold(imgray.copy(),254,255,2)
contours,_ = cv2.findContours(binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
mask = np.zeros(imgray.shape, dtype='uint8')

#Find the hole in the network
for i in range(len(contours)):
    area = cv2.contourArea(contours[i])
    if(area >= area_min and area < area_mix): #The in the range of Area
        c_min = []
        c_min.append(contours[i])
        cv2.drawContours(reults_img,c_min,-1,(246,235,123),-1)
        cv2.drawContours(reults_img,c_min,-1,(194,232,206),1)
        cv2.drawContours(mask,c_min, -1, 255, -1)
        
        #Marking the Holes
        M = cv2.moments(contours[i])
        cX = int(M['m10'] / M['m00'])
        cY = int(M['m01'] / M['m00'])
        area_holes.append(contours[i])
        cv2.putText(reults_img,str(len(area_holes)), (cX-20,cY+30),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255),3)
        cv2.putText(mask,str(len(area_holes)), (cX-20,cY+30),cv2.FONT_HERSHEY_SIMPLEX, 1, 255,3)
        continue
        

#Add all the nodes
for i in range (0,num_nodes): 
    cv2.circle(reults_img, all_nodes[i], 3,(94,183,183), -1, 0, 0)  #Add the node result
    cv2.circle(img, all_nodes[i], 3,(94,183,183), -1, 0, 0)  #Add the node network

#Create the result figure
plt.figure(num='Hole Detection in Sensor Network Project',
           figsize=(30,20),
           dpi=80)

plt.subplot(231),plt.imshow(img),plt.title('DRAW_NETWORK'),plt.axis('off')
plt.subplot(232),plt.imshow(cv2.bitwise_and(reults_img, reults_img, mask=mask)),plt.title('MASK'),plt.axis('off')
plt.subplot(233),plt.imshow(reults_img),plt.title('reults_IMG'),plt.axis('off')


data_info =str("Total Holes:" + str(len(contours))+
"\nThe Area of Holes Size:" + str(area_min) + "~" + str(area_mix)+
"\nThe Holes:" + str(len(area_holes))+
"\nThe image Size:" + str(img.shape))
plt.subplot(212),plt.text(0,0.8,data_info,size = 20,va = 'center'),plt.axis('off')
plt.subplots_adjust(hspace=0, wspace=0.01,bottom = 0)
plt.show()


print(data_info)
print ("DONE.")