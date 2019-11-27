import numpy as np
import pandas as pd
 
"""
    计算多边形的面积，包括非凸多边形的情况，
    要求输入的顶点是按照逆时针顺序顺次排列的。
    所要求解面积的多边形即为这些顶点一个一个地相连而成
    E = {<v0, v1>, <v1, v2>, <v2, v3>,...,<vn-2, vn-1>, <vn-1, v0>}
    @author: sdu_brz
    @date: 2019/02/18
"""
def getData():
    df = pd.read_csv("network_1", skiprows=1 ,sep=" ", header=None)
    xy = df.iloc[0:10]
    xy = xy.drop(columns=[0])
    xy = xy.to_numpy()
    
    
    edge = df.loc[11:27]
    edge = edge.drop(columns=[2])
    edge = edge.to_numpy()
    edge = edge.astype(np.int64)

def coss_multi(v1, v2):
    """
    计算两个向量的叉乘
    :param v1:
    :param v2:
    :return:
    """
    return v1[0]*v2[1] - v1[1]*v2[0]
 
 
def polygon_area(polygon):
    """
    计算多边形的面积，支持非凸情况
    :param polygon: 多边形顶点，已经进行顺次逆时针排序
    :return: 该多边形的面积
    """
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
    """测试"""
    #for
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


def main():
    global graph
    global cycles
    global xy
    xylist = {}
    area_list = {}
    
    for edge in graph:
        for node in edge:
            findNewCycles([node])
            
    for index in range(len(cycles)):
        node = cycles[index]
        xylist[index] = xy[node]
        area = polygon_area(xylist[index])
        if area > 0:
            area_list[index] = area
       
    print(area_list)

    
    
main()

