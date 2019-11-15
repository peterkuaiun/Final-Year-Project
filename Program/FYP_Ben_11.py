"""
Created on Mon Nov  11 12:48:43 2019

@author:     Ng Kim Hou
@Student ID: DB625369
@Description:


2019_UM_FST_CPS_FYP_Hole Detection in Sensor Network Project
FYP_11_11_2019
@author:     Ng Kim Hou
@Student ID: DB625369
@Description: 
1. Input the network data by using CNCAHNetGenerator
2. Draw the network form the data
3. Using OpenCV find the hole
4. Find all nodes in all holes
"""

import numpy as np
import cv2  

results_img = np.zeros((2100,2100, 3), np.uint8) #create a gray img
img = np.full((2100, 2100, 3), 255 ,np.uint8) #create a img
mask = np.zeros(cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY).shape,np.uint8)

#The node, edge and hole attributes
all_nodes = []
all_edges = []
all_holes = []
d = -4.99 #The distance which between the nodes and hole


#Read data file
def Read_data(fname):
    data_list = [] #The data list
    num_nodes = int
    all_nodes = []
    num_edges = int
    all_edges = []
    data_f = open(fname, 'r')
    for line in data_f.readlines():
        data_list.append(line.strip())
    
    num_nodes = int (data_list.pop(0)) #Pop out the number of nodes 
    #Get all the number node coordinate
    for i in range (0,num_nodes):
        node = data_list.pop(0) #Pop out the node coordinate
        node = node.split()
        node.pop(0) #Pop out the node index  
        all_nodes.append((int(float (node[0])*2000.0+50.0),int(float (node[1])*2000.0+50.0))) #(X, Y)  
    num_edges = int (data_list.pop(0)) #Pop out the number of edges 
    #Get all the edge
    for i in range (0,num_edges): 
        edge = data_list.pop(0) #Pop out the edge connection
        edge = edge.split()
        all_edges.append([int(edge[0]),int(edge[1])]) #(point 1, point 2)
    data_f.close
    return all_nodes,all_edges
    

def Hole_label(img,hole,t = "Hole"):
    M = cv2.moments(hole)
    cX = int(M['m10'] / M['m00'])
    cY = int(M['m01'] / M['m00'])
    cv2.putText(img,str(t), (cX,cY),cv2.FONT_HERSHEY_SIMPLEX, 1,(240,240,240),3,cv2.LINE_AA)
    return img

#Draw all the nodes
def Draw_AllNodes(img,all_nodes,color = (255,255,0),thickness=-1,lineType=0,shift=0):
    for i in range (0,int(len(all_nodes))): 
        cv2.circle(img, all_nodes[i], 8,color,thickness,lineType,shift)  #Add the node result
    return img

#Draw all the edges
def Draw_Alledges(img,all_nodes,all_edges,color = (100,0,100),thickness=3,lineType=8,shift=0):
    for i in range (0,int(len(all_edges))):
        cv2.line(img, all_nodes[all_edges[i][0]], all_nodes[all_edges[i][1]],color,thickness, lineType, shift)
    return img

#Draw one hole
def Draw_Hole(img,hole,color_1 = (100,205,40),color_2 = (0,0,255),area_min = 0,thickness=3,lineType=8,shift=0): 
    h = []
    h.append(hole)
    a = cv2.contourArea(hole)
    if (a >= area_min):
        cv2.drawContours(img,h,-1,color_1,-1)
        cv2.drawContours(img,h,-1,color_2,1,cv2.LINE_AA)
    return img


#Draw all the holes
def Draw_AllHoles(img,all_holes,color_1 = (100,205,40),color_2 = (0,0,255),thickness=3,shift=0,label = False):
    for i in range (0,int(len(all_holes))):
        hole = []
        hole.append(all_holes[i])
        Draw_Hole(img,hole,color_1,color_2,area_min,thickness,shift)
    if (label == True):
        for i in range (0,int(len(all_holes))):
                Hole_label(img,all_holes[i],str(i+1))
    return img

#Find the nodes of hole
def Find_HoleNodes(hole,all_nodes,img = " ",color = (0,200,0),thickness = 3,label = False):
    nodes_lst = []  #The nodes of hole 
    a = 0.0       #The return value of distance which between the nodes and hole in the image  
    for i in range (len(all_nodes)):
        a = cv2.pointPolygonTest(hole,all_nodes[i],True) 
        if (a >= d):
            nodes_lst.append(i)
            if (label == True):
                    cv2.circle(img, all_nodes[i], 14,color,thickness)  #Add the node result
    return nodes_lst

#Find all the nodes of holes
def Find_AllHolesNodes(all_holes,all_nodes,img = " ",color = (0,200,200),thickness = 3,label = False):
    holes_nodes = []  #The nodes of hole 
    for i in range (0,int(len(all_holes))):  
        holes_nodes.append(Find_HoleNodes(all_holes[i],all_nodes,img,color,thickness,label))
        if (label == True):
            print("The Hole %s:    Number of Nodes:%s"%(i+1,len(holes_nodes)))
        print("Node:%s"%(holes_nodes[i][:]))
    return holes_nodes,img

#Find the hole in Image Processing
def Find_holesIP(img):
    #Create the gray Image for Image Processing
    imgray = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY)
    _,binary = cv2.threshold(imgray.copy(),254,255,2)
    holes,_ = cv2.findContours(binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    holes = sorted(holes, key=cv2.contourArea)
    
    #Find the hole in the network
    for i in range(len(holes)-1):
        holeN_lst = []
        holeN_lst = Find_HoleNodes(holes[i],all_nodes)
        if(len(holeN_lst) > 3): #The in the range of Area
            all_holes.append(holes[i])
            continue
    return img,all_holes

#Main Program:
fname = 'data_1' #The data file name
out_format = '.png' #The output image format
#The size of Hole
area_min = 1000000 #(You may not use it.)

all_nodes,all_edges = Read_data(fname) #Read data
#Add all the edges    
Draw_Alledges(results_img,all_nodes,all_edges,(252, 121, 120))
#Find the hole in Image Processing
results_img = Find_holesIP(results_img)


results_img = img.copy()
Draw_Alledges(results_img,all_nodes,all_edges,(1,0,56),lineType= cv2.LINE_AA)
Draw_Alledges(img,all_nodes,all_edges,(1,0,56),lineType= cv2.LINE_AA)

for i in range(80,94):
    Draw_Hole(results_img,all_holes[i],color_1 = (200,200,200))
    Hole_label(results_img,all_holes[i],t = i)
    Draw_Hole(mask,all_holes[i],color_1 = (200,200,200))
    Hole_label(mask,all_holes[i],t = i)
 
#Add all the nodes
Draw_AllNodes(img,all_nodes,(200,100,255),lineType= cv2.LINE_AA);
Draw_AllNodes(results_img,all_nodes,(200,100,255),lineType= cv2.LINE_AA);
#Find_AllHolesNodes(all_holes,all_nodes,results_img,label = True)

'''  #Find all nodes in a Hole
#find the node of node:
mask_1 = np.zeros(img.shape, dtype='uint8')
Draw_AllHoles(mask_1,all_holes,label = True)
Draw_Alledges(mask_1,all_nodes,all_edges,(252, 121, 120),2,lineType = cv2.LINE_AA)
Draw_AllNodes(mask_1,all_nodes,(94,0,183),lineType= cv2.LINE_AA)
holes_nodes  = Find_AllHolesNodes(all_holes,all_nodes)

for i in range(0,len(holes_nodes)):
    print("The Hole %s:    Number of Nodes:%s"%(i+1,len(holes_nodes)))
    print("Node:%s"%(holes_nodes[i][:]))

plt.figure(num='Hole Detection in Sensor Network Project',
           figsize=(30,20),
           dpi=80)
plt.imshow(mask_1),plt.title('The Holes:'),plt.axis('off')
'''
#Save result Image
cv2.imwrite('ResultImage/result_'+fname+out_format, results_img)

'''
#Create the result figure
plt.figure(num='Hole Detection in Sensor Network Project',
           figsize=(30,20),
           dpi=80)

plt.subplot(231),plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)),plt.title('The NETWORK'),plt.axis('off')
plt.subplot(232),plt.imshow(cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)),plt.title('MASK'),plt.axis('off')
plt.subplot(233),plt.imshow(cv2.cvtColor(results_img, cv2.COLOR_BGR2RGB)),plt.title('results:'),plt.axis('off')


data_info =str("Number of Nodes:"+str(len(all_nodes))+
               "\nNumber of Edges:"+str(len(all_edges))+
                "\nTotal Holes:" + str(len(all_holes))+
                "\nThe Area of Holes Size:" + str(area_min)+
                "\nThe Holes:" + str(len(all_holes))+
                "\nThe image Size:" + str(img.shape))
plt.subplot(212),plt.text(0,0.8,data_info,size = 20,va = 'center'),plt.axis('off')
plt.subplots_adjust(hspace=0, wspace=0.01,bottom = 0)
plt.show()
'''

def mouse_click(event,x,y,flags,param):
    if event == 1:
        cv2.imshow(win_name, results_img)
    elif event == 2:
        cv2.imshow(win_name, img)
    elif event == 7:
        cv2.imshow(win_name, mask)


win_name = 'Hole Detection in Sensor Network Project'
cv2.namedWindow(win_name,0)
cv2.resizeWindow(win_name, 1000, 1000);
cv2.imshow(win_name, img)
cv2.setMouseCallback(win_name, mouse_click)
cv2.waitKey(0)
cv2.destroyAllWindows()

#print(data_info)
print ("DONE.")