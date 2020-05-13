import numpy as np
import cv2  
import os



#The node, edge and hole attributes
all_nodes = []
all_edges = []
all_holes = []
d = -4.99 #The distance which between the nodes and hole
area_min = 1000 #(You may not use it.)

name = 'n=1000d=6_ver2'
size = 2100

results_img = np.zeros((size,size, 3), np.uint8) #create a gray img
img = np.full((size, size, 3), 255 ,np.uint8) #create a img
mask = np.zeros(cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY).shape,np.uint8)

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
        all_nodes.append((int(float (node[0])*3.5),int(float (node[1])*3.5))) #(X, Y) 
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
    a = cv2.contourArea(hole)
    h = []
    h.append(hole)
    if (int(a) >= area_min):
        cv2.drawContours(img,h,-1,color_1,-1)
        cv2.drawContours(img,h,-1,color_2,1,cv2.LINE_AA)
    return img


#Draw all the holes ####Draw_AllHoles(results_img,all_holes[i],color_1 = (200,200,200),label = True)
def Draw_AllHoles(img,all_holes,color_1 = (100,205,40),color_2 = (0,0,255),thickness=3,shift=0,label = False):
    for i in range (0,int(len(all_holes))):
        Draw_Hole(img,all_holes[i],color_1,color_2,area_min,thickness,shift)
    
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
def Find_AllHolesNodes(all_holes,all_nodes,img = " ",color = (0,200,200),thickness = 3,label = False,sf = False):
    holes_nodes = []  #The nodes of hole
    if (sf == True):
        f = open((fname +"-node"+".txt"),'w')
    #with open(r'D:\result data\FD\Sparse\FR\n=2000d=6\node id\\' + 'n=2000d=6' + '.txt','w') as f:
    with open(r'D:\result data\test\node id\\' + name + '.txt','w') as f:
        for i in range (0,int(len(all_holes))):
            holes_nodes.append(Find_HoleNodes(all_holes[i],all_nodes,img,color,thickness,label))
            if (label == True):
                print("The Hole %s:    Number of Nodes:%s"%(i+1,len(holes_nodes)))
            if (sf == True):
                f.write((str(i+1) + "\n"))
                f.write("%s "%(holes_nodes[i][:]))
                f.write("\n")
                if (i == len(all_holes)):
                    f.close()
            #print("%s"%(holes_nodes[i][:]))
            f.write("%s"%(holes_nodes[i][:]))
            f.write("\n")
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
out_format = '.png' #The output image format
fname = os.path.abspath(r'C:\Users\peter\Desktop\test.txt') #The data file name

print(fname)
#The size of Hole
all_nodes,all_edges = Read_data(fname) #Read data
#Add all the edges    
Draw_Alledges(results_img,all_nodes,all_edges,(252, 121, 120))
#Find the hole in Image Processing
results_img = Find_holesIP(results_img)


results_img = img.copy()
Draw_Alledges(results_img,all_nodes,all_edges,(1,0,56),lineType= cv2.LINE_AA)
Draw_Alledges(img,all_nodes,all_edges,(1,0,56),lineType= cv2.LINE_AA)


Draw_AllHoles(results_img,all_holes,color_1 = (200,200,200),label = True)
Draw_AllHoles(mask,all_holes,color_1 = (200,200,200),label = True) 
#Find_AllHolesNodes(all_holes,all_nodes,sf = True)
#Add all the nodes
Draw_AllNodes(img,all_nodes,(200,100,255),lineType= cv2.LINE_AA);
Draw_AllNodes(results_img,all_nodes,(200,100,255),lineType= cv2.LINE_AA);
#Find_AllHolesNodes(all_holes,all_nodes,results_img,label = True)

#Find all nodes in a Hole
#find the node of node:
mask_1 = np.zeros(img.shape, dtype='uint8')
Draw_AllHoles(mask_1,all_holes,label = True)
Draw_Alledges(mask_1,all_nodes,all_edges,(252, 121, 120),2,lineType = cv2.LINE_AA)
Draw_AllNodes(mask_1,all_nodes,(94,0,183),lineType= cv2.LINE_AA)

#holes_nodes  = Find_AllHolesNodes(all_holes,all_nodes)

#Save result Image
cv2.imwrite(r'C:\Users\peter\Desktop\result\\' + name + out_format, results_img)

win_name = 'Hole Detection in Sensor Network Project'
cv2.namedWindow(win_name,0)
cv2.resizeWindow(win_name, 1000, 1000);
cv2.imshow(win_name, results_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
#print(data_info)

print ("DONE.")