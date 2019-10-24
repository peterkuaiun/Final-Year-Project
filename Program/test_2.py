"""
Created on Wed Oct  9 18:54:43 2019

@author:     Ng Kim Hou
@Student ID: DB625369
@Description:
    
"""

import networkx as nx
import matplotlib.pyplot as plt
#建立一个空的无向图G
G = nx.Graph()
#添加一个节点1
G.add_node(1)
#添加一条边2-3（隐含着添加了两个节点2、3）
G.add_edge(2,3)
#对于无向图，边3-2与边2-3被认为是一条边
G.add_edge(3,2)
#输出全部的节点： [1, 2, 3]
print (G.nodes())
#输出全部的边：[(2, 3)]
print (G.edges())
#输出边的数量：1
print (G.number_of_edges())
#输出点数
print (G.number_of_nodes())
nx.draw(G, with_labels=True)
plt.show()
