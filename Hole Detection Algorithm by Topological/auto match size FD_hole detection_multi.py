import numpy as np
import cv2  
import os
import time

results_img = np.zeros((4200,4200, 3), np.uint8) #create a gray img
img = np.full((4200, 4200, 3), 255 ,np.uint8) #create a img
mask = np.zeros(cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY).shape,np.uint8)

#The node, edge and hole attributes
all_nodes = []
all_edges = []
all_holes = []
d = -4.99 #The distance which between the nodes and hole
area_min = 1000 #(You may not use it.)


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
        all_nodes.append((int(float (node[0])*size[1]),int(float (node[1])*size[1]))) #(X, Y) 
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
    #with open(r'D:\result data\FD\Sparse\FR\\'+ name +'\\node id\\' + name + '.txt','w') as f:
    nodeidpath = (outputpath + 'node id\\')       
    if not os.path.exists(nodeidpath):
        os.makedirs(nodeidpath)
    
    with open(nodeidpath + folder3 + '.txt' ,'w') as f:
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

def readData(fname):
    data_list = []
    data_f = open(fname)
    for line in data_f.readlines():
        nums = line.strip().split(',')
        nums = [item.replace('[', '').replace(']', '').replace(' ', '') for item in nums]
        nums = [int(x) for x in nums]
        matrix = np.array(nums)
        matrix = matrix.transpose()
        MatToList = matrix.tolist()
        for i in range(len(MatToList)):
            #print(MatToList[i])
            data_list.append(MatToList[i])

    return data_list

def calAcc(orig_set, FD_set):
    allnode = list(range(1,501))
    #read data
    orig_list = readData(orig_set)
    FD_list = readData(FD_set)
    #calulate TP and TN, find the duplicate node id will get TP
    t_intersection = list(set(orig_list).intersection(set(FD_list)))
    TP = len(t_intersection)
    TN = len(orig_list) - TP
    #find the difference node id between the node in the hole and all node, will get the the node id out of the hole
    orig_list_outside = list(set(orig_list).symmetric_difference(set(allnode)))
    FD_list_outside = list(set(FD_list).symmetric_difference(set(allnode)))
    #calulate FP and FN, find the duplicate node id will get FP
    f_intersection = list(set(orig_list_outside).intersection(set(FD_list_outside)))
    FP = len(f_intersection)
    FN = len(FD_list_outside) - FP
    #confusion matrix accuracy formula
    acc = (TP + TN) / (TP + TN + FP + FN)
    #print('TP:', TP,' TN:', TN, ' FP:', FP, ' FN:',FN)
    with open(r'D:\result data\performance evaluation criteria\Sparse\FR\\' + fname + '.txt','w') as f:
        #f.write("%s"%(holes_nodes[i][:]))
        f.write('TP:'+ str(TP))
        f.write(' TN:'+ str(TN))
        f.write(' FP:'+ str(FP))
        f.write(' FN:'+ str(FN))
        f.write(' Acc:' + str(acc))

    return acc

def findSize(fname):
    node_num = int(folder3.split('d')[0].split('=')[1])
    if node_num == 500 or node_num == 1000:
        return 2100, 3.5
    elif node_num == 2000:
        return 4200, 7
    elif node_num == 3000:
        return 6300, 10.5
    elif node_num == 5000:
        return 10500, 17.5
    elif node_num == 7000:
        return 14700, 24.5
    elif node_num == 10000:
        return 21000, 35

#Main Program:
out_format = '.png' #The output image format
#folderlist = ['Sparse', 'Uniform']
#folderlist = (r'D:\data_600s\dataset\\')
folderpath = (r'D:\data_600s\result\\')
folderlist = os.listdir(folderpath)
for folder in folderlist:
    
    folderpath2 = (folderpath + folder + '\\')
    folderlist2 = os.listdir(folderpath2)

    for folder2 in folderlist2:
        folderpath3 = (folderpath2 + folder2 + '\\')
        
        folderlist3 = os.listdir(folderpath3)
        for folder3 in folderlist3:
            folder3list = (folderpath3 + folder3 + '\\graph')
            
            allFileList = os.listdir(folder3list)
            allFileList.sort(key= lambda x:int(x[:-4]))
            fname = allFileList[-1]
            print(folder3list)
            print(fname)
            now = int(round(time.time()*1000))
            thetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
            print('Start time:', thetime)

            all_nodes.clear() 
            all_edges.clear()
            all_holes.clear()
            
            size = findSize(fname)
            results_img = np.zeros((size[0],size[0], 3), np.uint8) #create a gray img
            img = np.full((size[0], size[0], 3), 255 ,np.uint8) #create a img
            mask = np.zeros(cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY).shape,np.uint8)
            outputpath = (r'D:\result data\FD\\' + folder + '\\' + folder2 + '\\' + folder3 + '\\')
            
            if not os.path.exists(outputpath):
                os.makedirs(outputpath)
            
            #The size of Hole
            all_nodes,all_edges = Read_data(os.path.join(folder3list, fname)) #Read data
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
            
            holes_nodes = Find_AllHolesNodes(all_holes,all_nodes)
        
            #Save result Image
            cv2.imwrite(outputpath + os.path.splitext(fname)[0] + out_format, results_img)
            
print ("DONE.")