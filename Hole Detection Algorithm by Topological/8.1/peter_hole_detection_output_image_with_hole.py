import numpy as np
import cv2 
import sys 
#import time

#The node, edge and hole attributes

fname = str(sys.argv[1])
output_file_name = str(sys.argv[2])

#Read data file
def readData(fname):
    data_list = [] #The data list
    num_nodes = int
    all_nodes = []
    num_edges = int
    all_edges = []
    node_x = []
    node_y = []
    data_f = open(fname, 'r')
    for line in data_f.readlines():
        data_list.append(line.strip())
    
    num_nodes = int (data_list.pop(0)) #Pop out the number of nodes 
    #Get all the number node coordinate
    for i in range (0,num_nodes):
        node = data_list.pop(0) #Pop out the node coordinate
        node = node.split()
        node.pop(0) #Pop out the node index  
        node_x.append(node[0])
        node_y.append(node[1])
    #Change it to list    
    node_x = list(map(float, node_x))
    node_y = list(map(float, node_y))
    #Find the minimun value in x and y list
    min_x = min(node_x)
    min_y = min(node_y)
    #If the coorodinate of nodes are nagative, change it to be positive
    if min_x or min_y < 0:
        for i in range (0,num_nodes):
            node_x[i] = node_x[i] + min_x * -1
            node_y[i] = node_y[i] + min_y * -1
    #Find the maximun value in x and y list        
    max_x = max(node_x)
    max_y = max(node_y)
    #Calulate the canvas size by the node numbers and radius of node
    canvas_size = (4 * num_nodes)
    #Calulate the ratio for enlarge the coorodinate of node that fitting the canvas size
    node_ratio = (min((canvas_size / max_x), (canvas_size / max_y)))
    #print(node_ratio)
    #Origin coordinates
    xc = 0
    yc = 0
    
    for i in range (0,num_nodes):
        x = int(xc + node_ratio * (node_x[i] - xc))
        y = int(yc + node_ratio * (node_y[i] - yc))
        all_nodes.append((x, y)) #(X, Y) 
    
    num_edges = int (data_list.pop(0)) #Pop out the number of edges 
    #Get all the edge
    for i in range (0,num_edges): 
        edge = data_list.pop(0) #Pop out the edge connection
        edge = edge.split()
        all_edges.append([int(edge[0]),int(edge[1])]) #(point 1, point 2)
    data_f.close
    
    area_min_radio = 5000 / 4000
    area_min = area_min_radio * canvas_size
    
    return all_nodes, all_edges, num_nodes, canvas_size, area_min

#Lable the hole
def holeLabel(img,hole,t = "Hole"):
    M = cv2.moments(hole)
    cX = int(M['m10'] / M['m00'])
    cY = int(M['m01'] / M['m00'])
    cv2.putText(img,str(t), (cX,cY),cv2.FONT_HERSHEY_SIMPLEX, 1,(240,240,240),3,cv2.LINE_AA)
    
    return img

#Draw all the nodes
def drawAllNodes(img,all_nodes,color = (255,255,0),thickness=-1,lineType=0,shift=0):
    for i in range (0,int(len(all_nodes))): 
        cv2.circle(img, all_nodes[i], 8,color,thickness,lineType,shift)  #Add the node result
        
    return img

#Draw all the edges
def drawAlledges(img,all_nodes,all_edges,color = (100,0,100),thickness=3,lineType=8,shift=0):
    for i in range (0,int(len(all_edges))):
        cv2.line(img, all_nodes[all_edges[i][0]], all_nodes[all_edges[i][1]],color,thickness, lineType, shift)
        
    return img

#Draw one hole
def drawHole(img,hole,color_1 = (100,205,40),color_2 = (0,0,255),area_min = 0,thickness=3,lineType=8,shift=0): 
    area = cv2.contourArea(hole)
    h = []
    h.append(hole)
    if (int(area) >= area_min):
        cv2.drawContours(img,h,-1,color_1,-1)
        cv2.drawContours(img,h,-1,color_2,1,cv2.LINE_AA)
        
    return img


#Draw all the holes ####Draw_AllHoles(results_img,all_holes[i],color_1 = (200,200,200),label = True)
def drawAllHoles(img,all_holes,color_1 = (100,205,40),color_2 = (0,0,255),thickness=3,shift=0,label = False):
    for i in range (0,int(len(all_holes))):
        drawHole(img,all_holes[i],color_1,color_2,area_min,thickness,shift)
    
    if (label == True):
        for i in range (0,int(len(all_holes))):
                holeLabel(img,all_holes[i],str(i+1))
    return img

#Find the nodes of hole
def findHoleNodes(hole,all_nodes,img = " ",color = (0,200,0),thickness = 3,label = False):
    nodes_lst = []  #The nodes of hole 
    a = 0.0         #The return value of distance which between the nodes and hole in the image  
    d = -4.99       #The distance which between the nodes and hole
    for i in range (len(all_nodes)):
        a = cv2.pointPolygonTest(hole,all_nodes[i],True) 
        if (a >= d):
            nodes_lst.append(i)
            if (label == True):
                    cv2.circle(img, all_nodes[i], 14,color,thickness)  #Add the node result
                                      
    return nodes_lst

#Find all the nodes of holes
def findAllHolesNodes(all_holes,all_nodes,img = " ",color = (0,200,200),thickness = 3,label = False,sf = False):
    holes_nodes = []  #The nodes of hole
    with open(output_file_name ,'w') as f:
        f.write("%s\n"%num_nodes)
        for i in range (0,int(len(all_holes))):
            holes_nodes.append(findHoleNodes(all_holes[i],all_nodes,img,color,thickness,label))
            f.write("%s\n"%(holes_nodes[i][:]))
    return holes_nodes,img

#Find the hole in Image Processing
def findHolesIP(img):
    #Create the gray Image for Image Processing
    imgray = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY)
    _,binary = cv2.threshold(imgray.copy(),254,255,2)
    holes,_ = cv2.findContours(binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    
    tmp = [x for x in holes if not (cv2.contourArea(x) < area_min)]      
    holes = sorted(tmp, key=cv2.contourArea)
    
    #Find the hole in the network
    for i in range(len(holes)-1):
        holeN_lst = []
        holeN_lst = findHoleNodes(holes[i],all_nodes)
        if(len(holeN_lst) > 3): #The in the range of Area
            all_holes.append(holes[i])
            continue
        
    return img,all_holes

#Main Program:
input_list = []
node_list = []

#print(fname)
#print(output_file_name)

#time_start = time.time()

all_nodes = []
all_edges = []
all_holes = []
holes_nodes = []

#Read data
all_nodes, all_edges, num_nodes, canvas_size, area_min = readData(fname) 

results_img = np.zeros((canvas_size,canvas_size, 3), np.uint8) #create a gray img
img = np.full((canvas_size, canvas_size, 3), 255 ,np.uint8) #create a img
mask = np.zeros(cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY).shape,np.uint8)

#Add all the edges    
drawAlledges(results_img,all_nodes,all_edges,(252, 121, 120))

#Find the hole in Image Processing
results_img = findHolesIP(results_img)

results_img = img.copy()

#Draw all the edge
drawAlledges(results_img,all_nodes,all_edges,(1,0,56),lineType= cv2.LINE_AA)
drawAlledges(img,all_nodes,all_edges,(1,0,56),lineType= cv2.LINE_AA)

#Draw all the hole
drawAllHoles(results_img,all_holes,color_1 = (200,200,200),label = True)
drawAllHoles(mask,all_holes,color_1 = (200,200,200),label = True) 

#Draw all the node
drawAllNodes(img,all_nodes,(200,100,255),lineType= cv2.LINE_AA);
drawAllNodes(results_img,all_nodes,(200,100,255),lineType= cv2.LINE_AA);
#Find_AllHolesNodes(all_holes,all_nodes,results_img,label = True)

#find the node of node:
mask_1 = np.zeros(img.shape, dtype='uint8')
drawAllHoles(mask_1,all_holes,label = True)
drawAlledges(mask_1,all_nodes,all_edges,(252, 121, 120),2,lineType = cv2.LINE_AA)
drawAllNodes(mask_1,all_nodes,(94,0,183),lineType= cv2.LINE_AA)

cv2.imwrite(output_file_name, results_img)
#Find all nodes in a Hole
#holes_nodes  = findAllHolesNodes(all_holes,all_nodes)
#End of time
#time_end = time.time()
#print('It cost %f seconds' % (time_end - time_start))
#print ("DONE.")