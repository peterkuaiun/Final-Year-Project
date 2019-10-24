"""
Created on Wed Oct  9 22:32:11 2019

@author:     Ng Kim Hou
@Student ID: DB625369
@Description:
    
"""

#from PIL import Image
#import cv2 as cv
#import numpy as np

#import matplotlib.pyplot as plt
#import networkx as nx

'''
#Creat The Network
all_nodes = [[1,2],[2,5],[5,6],[3,1],[0,1]]
G = nx.Graph()
G.add_node(1,pos = (all_nodes[0]))
G.add_node(2,pos = (all_nodes[1]))
G.add_node(3,pos = (all_nodes[2]))
G.add_node(4,pos = (all_nodes[3]))
G.add_node(5,pos = (all_nodes[4]))
G.add_edge(1,2)
G.add_edge(2,3)
G.add_edge(3,4)
G.add_edge(4,5)
G.add_edge(5,1)
#Show the result
print ('Number of edges:',G.number_of_edges())
print ('Number of nodes:',G.number_of_nodes())
plt.figure(3,figsize=(4,4))
for i in range(0,5):
    plt.plot(all_nodes[i][0],all_nodes[i][1])
#nx.draw(G,nx.get_node_attributes(G, 'pos'),node_size=30) #draw the network in the graphic G
#nx.draw_spectral(G)
#nx.connected_components(G)
#G.area(colormap = 'Greens_r')
#nx.draw_spring(G, "#E0F5B9")
plt.figure(3,figsize=(4,4))
plt.draw()

'''
import numpy as np
import matplotlib.pyplot as plt
#y=np.arange(5)
plt.plot([2,5],[0.2,0.22],marker='o')
plt.plot(1,2,'o')
#plt.plot(y+2,marker='^')
#plt.plot(y+3,'*')
plt.show()