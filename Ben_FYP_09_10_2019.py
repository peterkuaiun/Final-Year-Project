"""
Created on Mon Oct  9 16:21:49 2019

2019_UM_FST_CPS_FYP_Hole Detection in Sensor Network Project
FYP_09_10_2019
@author:     Ng Kim Hou
@Student ID: DB625369
@Description: 
1. Input the network data by using CNCAHNetGenerator
2. Find all the node and edges
3. Draw back the network
   
"""
#from PIL import Image
#import cv2 as cv
#import numpy as np

import matplotlib.pyplot as plt
import networkx as nx
#import pyglet as


fname = 'data_5' #The data file name
out_format = '.png' #The output image format
data_list = list() #The data list

#The node and edge attributes
num_nodes = int
all_nodes = list()
num_edges = int
all_edges = list()

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
    all_nodes.append([float (node[0]),float (node[1])]) #(X, Y)
  
num_edges = int (data_list.pop(0)) #Pop out the number of edges 

#Get all the edge
for i in range (0,num_edges): 
    edge = data_list.pop(0) #Pop out the edge connection
    edge = edge.split()
    all_edges.append([int(edge[0]),int(edge[1])]) #(point 1, point 2)

#Creat The Network
G = nx.Graph()  #Creat blank graphic

#Add all the nodes
for i in range (0,num_nodes):
    G.add_node(i,pos = (all_nodes[i][0],all_nodes[i][1])) #Add the node coordinate by index i

#Add all the edges
for i in range (0,num_edges):
    G.add_edge(all_edges[i][0],all_edges[i][1]) #Add the edge connection

#Show the result
print ('Number of edges:',G.number_of_edges())
print ('Number of nodes:',G.number_of_nodes())
plt.figure(3,figsize=(12,12))
nx.draw(G,nx.get_node_attributes(G, 'pos'),node_size=30) #draw the network in the graphic G
plt.savefig((fname+out_format), format="PNG") #Save the figure


plt.show()

print('DONE')
