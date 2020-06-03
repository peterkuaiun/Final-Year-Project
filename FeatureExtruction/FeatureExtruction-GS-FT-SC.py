"""
Created on Sat May 30 21:51:50 2020
2019_UM_FST_CPS_FYP_Hole Detection in Sensor Network Project
FYP_30_05_2020
@author:     Ng Kim Hou
@Student ID: DB625369
@Description: 



Readme:
genrate hole training Image by Graph Segmentation and Feature Transformation with Specific Classification



"""

import numpy as np
import cv2  
import random
import os
import glob

d =-4.999999 #The distance which between the nodes and hole
area_min = 1000 #(You may not use it.)

"""
class:
0 4-node-hole
1 5-node-hole
2 6-node-hole
3 7-node-hole
4 8-node-hole
5 9-node-hole

"""



#Read data file, It is for ground truth sensor network.
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
    img_size = num_nodes * 4
    #Get all the number node coordinate
    for i in range (0,num_nodes):
        node = data_list.pop(0) #Pop out the node coordinate
        node = node.split()
        node.pop(0) #Pop out the node index  
        all_nodes.append((int(float (node[0])*float(img_size-100)+50.0),int(float (node[1])*float(img_size-100)+50.0))) #(X, Y)  
    num_edges = int (data_list.pop(0)) #Pop out the number of edges 
    #Get all the edge
    for i in range (0,num_edges): 
        edge = data_list.pop(0) #Pop out the edge connection
        edge = edge.split()
        all_edges.append([int(edge[0]),int(edge[1])]) #(point 1, point 2)
    data_f.close
    return all_nodes,all_edges,img_size
    

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
        cv2.drawContours(img,h,-1,color_2,thickness,cv2.LINE_AA)
    return img


#Draw all the holes ####Draw_AllHoles(results_img,all_holes[i],color_1 = (200,200,200),label = True)
def Draw_AllHoles(img,all_holes,color_1 = (100,205,40),color_2 = (0,0,255),thickness=3,shift=0,label = False):
    for i in range (0,int(len(all_holes))):
        Draw_Hole(img,all_holes[i],color_1,color_2,area_min,thickness,shift)
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


#Find the hole in Image Processing
def Find_holesIP(img,all_nodes,all_holes):
    #Create the gray Image for Image Processing
    imgray = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY)
    _,binary = cv2.threshold(imgray.copy(),254,255,2)
    holes,_ = cv2.findContours(binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    holes = sorted(holes, key=cv2.contourArea)
    
    #Find the hole in the network
    for i in range(len(holes)-1):
        holeN_lst = []
        holeN_lst = Find_HoleNodes(holes[i],all_nodes)
        if(len(holeN_lst) >=4): #The in the range of Area
            all_holes.append(holes[i])
            continue
    return img,all_holes

#This the Feature Extraction code
#fname means the path of sensor network; count_t is count the number of each classes;
#s mean the symbol of the training image. for example:s = "u",the output image = u0001.jpg
def gen_img(fname,count_t,s = ""): 
    print('[INFO] Graph Segmentation and Feature Transformation with Specific Classification')
    print("[LOADING]:%s"%fname)
    class_path = ["4-nodes-hole/","5-nodes-hole/","6-nodes-hole/","simple-polygon-hole/","sensor_network/"]
    
    #Genrate the path of Training dataset
    if not os.path.exists('TrainingImages/'):
        os.makedirs('TrainingImages/%s' %class_path[0])
        os.makedirs('TrainingImages/%s' %class_path[1])
        os.makedirs('TrainingImages/%s' %class_path[2])
        os.makedirs('TrainingImages/%s' %class_path[3])
        os.makedirs('TrainingImages/%s' %class_path[4])
    if not os.path.exists('TrainingImages/%s' %class_path[0]):
        os.makedirs('TrainingImages/%s' %class_path[0])
    if not os.path.exists('TrainingImages/%s' %class_path[1]):
        os.makedirs('TrainingImages/%s' %class_path[1])
    if not os.path.exists('TrainingImages/%s' %class_path[2]):
        os.makedirs('TrainingImages/%s' %class_path[2])
    if not os.path.exists('TrainingImages/%s' %class_path[3]):
        os.makedirs('TrainingImages/%s' %class_path[3])
    if not os.path.exists('TrainingImages/%s' %class_path[4]):
        os.makedirs('TrainingImages/%s' %class_path[4])

    all_nodes = []
    all_edges = []
    all_holes = []

    all_nodes,all_edges,img_size = Read_data(fname) #Read data
    #Add all the edges
    results_img = np.zeros((img_size,img_size, 3), np.uint8) #create a gray img
    img = np.full((img_size, img_size, 3), 255 ,np.uint8) #create a img
    Draw_Alledges(results_img,all_nodes,all_edges,(252, 121, 120))
    #cv2.imshow("A",results_img)
    results_img,all_holes = Find_holesIP(results_img,all_nodes,all_holes)
    Draw_Alledges(img,all_nodes,all_edges,(1,0,56),lineType= cv2.LINE_AA)
    #Add all the nodes
    Draw_AllNodes(img,all_nodes,(200,100,255),lineType= cv2.LINE_AA)
    
    #Genrate sensor network
    name_3 = './TrainingImages/'+class_path[4] +os.path.basename(fname)+"-"+str(s) 
    cv2.imwrite(name_3+'.jpg',img)
    of = open(name_3+".txt", "w")
    #print(len(all_nodes))
    for i in range(len(all_holes)):
        #print("b")
        the_hole=[]
        the_hole=all_holes[i]
        color_b = np.random.randint(0,high = 256,size = (3,)).tolist()
        cropped_ft = np.full((img_size, img_size, 3), color_b ,np.uint8)
        cropped_gs = np.full((img_size, img_size, 3), color_b ,np.uint8)
        ard_node = Find_HoleNodes(the_hole,all_nodes,all_holes)
        
        if len(ard_node)>6:
            classes = 3
        else:
            classes = len(ard_node) - 4
        
        x,y,w,h = cv2.boundingRect(the_hole)
        o_x = (x+w)/2 * 1.0 / img_size
        o_y = (y+h)/2 * 1.0 / img_size
        o_w = (w+20) * 1.0 / img_size
        o_h = (h+20) * 1.0 / img_size
        of.write("%d %f %f %f %f\n" %(classes,o_x,o_y,o_w,o_h))
        
####Feature Transformation
        
        count_t[classes]+=1
        name_0 = './TrainingImages/'+class_path[classes] +str(s)+str(count_t[classes]).zfill(4)
        color_n = np.random.randint(50,high = 200,size = (3,)).tolist()
        r = np.random.randint(5,8)
        Draw_Hole(cropped_ft,the_hole,(255,255,255),(1,0,56),thickness=2,lineType= cv2.LINE_AA) 
        for n in range(0,len(ard_node)):
            cv2.circle(cropped_ft, all_nodes[ard_node[n]], r,color_n,-1, cv2.LINE_AA , 0)
        cropped_ft = cropped_ft[(y-50):(y+h+50), (x-50):(x+w+50)]
        
        i_h, i_w,_ = cropped_ft.shape
        o_x = i_w/2 * 1.0 /i_w
        o_y = i_h/2 * 1.0 /i_h
        o_w = (w+20) * 1.0 / i_w
        o_h = (h+20) * 1.0 / i_h

        cv2.imwrite(name_0+'.jpg',cropped_ft)
        with open(name_0+".txt","w") as f:
            f.write("%d %f %f %f %f" %(classes,o_x,o_y,o_w,o_h)) #If u only want to train one classes, let classes = '0'
        
####Feature Transformation
            
####Graph Segmentation

        count_t[classes]+=1
        name_1 = './TrainingImages/'+class_path[classes] +str(s)+str(count_t[classes]).zfill(4)
        cropped_gs = img[(y-50):(y+h+50), (x-50):(x+w+50)]
        cv2.imwrite(name_1+'.jpg',cropped_gs)
        i_h, i_w,_ = cropped_ft.shape
        o_x = i_w/2 * 1.0 /i_w
        o_y = i_h/2 * 1.0 /i_h
        o_w = (w+20) * 1.0 / i_w
        o_h = (h+20) * 1.0 / i_h
        with open(name_1+".txt","w") as f:
            f.write("%d %f %f %f %f" %(classes,o_x,o_y,o_w,o_h)) #If u only want to train one classes, let classes = '0'
        
####Graph Segmentation

    print ("[DONE] %s Graph Segmentation and Feature Transformation DONE.\n"%os.path.basename(fname))
    of.close()


#Genrate the path of those object classes to train/valid  .txt
def output_train_test_txt(path = 'TrainingImages\\',train_txt= "train.txt",test_txt="test.txt",count_t=0):
    print('[INFO] Output train.txt and test.txt')
    print('[LOADING] %s '%path)
    file_base_path = os.path.basename(os.getcwd())
    cont =0
    count_1 = 0
    os.listdir(path)
    with open(train_txt, 'w') as tef:
        for jpg_file in glob.glob(path + '*.jpg'):
            count_1 += 1
            if cont ==5:
                cont =0
            else:
                if (count_1==len(glob.glob(path + '*.jpg'))):
                    tef.write('%s\\%s'%(file_base_path,jpg_file))
                else:
                    tef.write('%s\\%s\n'%(file_base_path,jpg_file))
                cont +=1
    tef.close()            
    cont =0
    count_1 =0
    with open(test_txt, 'w') as tef:
        for jpg_file in glob.glob(path + '*.jpg'):
            count_1 += 1
            if cont ==5:
                if (count_1>=len(glob.glob(path + '*.jpg'))-5):
                    tef.write('%s\\%s'%(file_base_path,jpg_file))
                else:
                    tef.write('%s\\%s\n'%(file_base_path,jpg_file))
                cont =0
            else:
                cont +=1
    tef.close()
    print('[DONE] Train.txt and Test.txt Done.\n')


#Merge the path train/valid dataset .txt
def MergeTxt(filepath,outfile): 
    print('[INFO] Merge .txt')
    k = open(outfile, 'a+')   
    for filenames in filepath:
        print('[LOADING] %s'%filenames)
        f = open(filenames)
        k.write(f.read()+"\n")
    k.close()
    print('[DONE] Merge [%s] done.\n' %outfile)



#Main Program:
#Genrate and detect sensor network
path = input("Input the sensor network path:")
path  = path.split()

sn_type = input('Input each sensor network type (Sparse input s; Uniform input u; Other input a):')
sn_type  = sn_type.split()
for i in range(0,len(path)):
    dirs_path = os.listdir(path[i]) #The path of sensor network 
    count_t=[0,0,0,0]
    for j in dirs_path:
        fname = path[i]+str(j)
        gen_img(fname,count_t,sn_type[i])
        print(path[i],sn_type[i])
        print('{INFO]The sensor network has: 4-nodes-hole %d, 5-nodes-hole %d,6-nodes-hole %d, simple-polygon-hole %d' 
        %(count_t[0],count_t[1],count_t[2],count_t[3]))
    
#output each classes train.txt and test.txt from the Training Image path
output_train_test_txt('TrainingImages\\4-nodes-hole\\','4-train.txt','4-test.txt') 
output_train_test_txt('TrainingImages\\5-nodes-hole\\','5-train.txt','5-test.txt')
output_train_test_txt('TrainingImages\\6-nodes-hole\\','6-train.txt','6-test.txt')
output_train_test_txt('TrainingImages\\simple-polygon-hole\\','7-train.txt','7-test.txt')
output_train_test_txt('TrainingImages\\sensor_network\\','sn-train.txt','sn-test.txt')

##Merge those classes train.txt and test.txt be the final train.txt and test.txt
filepath = ['4-train.txt','5-train.txt','6-train.txt','7-train.txt','sn-train.txt']
MergeTxt(filepath,'hole-detection-yolov3-train.txt')

filepath = ['4-test.txt','5-test.txt','6-test.txt','7-test.txt','sn-test.txt']
MergeTxt(filepath,'hole-detection-yolov3-test.txt')

print ("[INFO]ALL DONE.")