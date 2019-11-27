import numpy as np
import pandas as pd
 
def getData():
    df = pd.read_csv("simple_graph", skiprows=1 ,sep=" ", header=None)
    xy = df.iloc[0:100]
    xy = xy.drop(columns=[0])
    xy = xy.to_numpy()
    
    edge = df.loc[101:501]
    edge = edge.drop(columns=[2])
    edge = edge.to_numpy()
    edge = edge.astype(np.int64)
    
    return edge, xy

def coss_multi(v1, v2):
    return v1[0]*v2[1] - v1[1]*v2[0]
 
 
def polygon_area(polygon):

    n = len(polygon)
 
    if n < 3:
        return 0
 
    vectors = np.zeros((n, 2))
    for i in range(0, n):
        vectors[i, :] = polygon[i, :] - polygon[0, :]
 
    area = 0
    for i in range(1, n):
        area = area + coss_multi(vectors[i-1, :], vectors[i, :]) / 2
 
    return area
 
 
def calCycleArea():  
    graph, xy = getData()
    polygon1 = xy
    print(polygon_area(polygon1))
    


def findNewCycles(path):
    start_node = path[0]
    next_node= None
    sub = []

    #visit each edge and each node of each edge
    for edge in graph:
        node1, node2 = edge
        if start_node in edge:
                if node1 == start_node:
                    next_node = node2
                else:
                    next_node = node1
                if not visited(next_node, path):
                        # neighbor node not on path yet
                        sub = [next_node]
                        sub.extend(path)
                        # explore extended path
                        findNewCycles(sub);
                elif len(path) > 2  and next_node == path[-1]:
                        # cycle found
                        p = rotate_to_smallest(path);
                        inv = invert(p)
                        if isNew(p) and isNew(inv):
                            cycles.append(p)

def invert(path):
    return rotate_to_smallest(path[::-1])

#  rotate cycle path such that it begins with the smallest node
def rotate_to_smallest(path):
    n = path.index(min(path))
    return path[n:]+path[:n]

def isNew(path):
    return not path in cycles

def visited(node, path):
    return node in path

def isInsidePolygon(pt, poly):
    c = False
    i = -1
    l = len(poly)
    j = l - 1
    while i < l - 1:
        i += 1
        #print(i, poly[i], j, poly[j])
        if ((poly[i][0] <= pt[0] and pt[0] < poly[j][0]) or (
                poly[j][0] <= pt[0] and pt[0] < poly[i][0])):
            if (pt[1] < (poly[j][1] - poly[i][1]) * (pt[0] - poly[i][0]) / (
                poly[j][0] - poly[i][0]) + poly[i][1]):
                c = not c
        j = i
    return c

graph, xy = getData()
cycles = []


def main():
    global graph
    global cycles
    global xy
    xylist = {}
    new_list = {}
    i = 0
        
    for edge in graph:
        for node in edge:
            findNewCycles([node])
            
    for index in range(len(cycles)):
        node = cycles[index]
        xylist[index] = xy[node]
        '''
        area = polygon_area(xylist[index])
        if area < 0:
            del xylist[index]
        '''
    #print(xylist)

    for index in range(len(xylist)):
        for xy_index in range(len(xy)):
            if isInsidePolygon(xy[xy_index], xylist[index]):
                del xylist[index]
                break
        
    print(len(xylist))

    for item in xylist:
        area = polygon_area(xylist[item])

        if area < 0:
            del xylist[index]
    
    for item in xylist:
        new_list[i] = cycles[item]
        i = i + 1
    
    print(new_list)
        
    #print(area_list)
    #print(new_list)
    #sort_list = sorted(area_list.items(), key=lambda item:item[1], reverse=True)
    #print(sort_list)
    

    
    
main()









