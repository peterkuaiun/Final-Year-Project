"""
Created on Tue Jun  2 22:05:20 2020

@author:     Ng Kim Hou
@Student ID: DB625369
@Description:
    -The Hole Detection in sensor network by CNN.
    -This code is for Ground truth sensor network.
    
"""
from utils import yolo
import os
import numpy as np
import cv2

def yolo_hole_detection(fname,yolo_cfg_loc,confidence = 0.25,threshold =0.001):

    if not os.path.exists('result/%s' %os.path.dirname(fname)):
        os.makedirs('result/%s' %os.path.dirname(fname))
        os.makedirs('result/%s/Explanations' %os.path.dirname(fname))
        os.makedirs('result/%s/hole-txt' %os.path.dirname(fname))
        
    if not os.path.exists('result/%s/Explanations' %os.path.dirname(fname)):
        os.makedirs('result/%s/Explanations' %os.path.dirname(fname))
    if not os.path.exists('result/%s/hole-txt' %os.path.dirname(fname)):
        os.makedirs('result/%s/hole-txt' %os.path.dirname(fname))


    pre_image_path = "result/%s.jpg" %(fname)
    hole_ana_path = "result/%s/Explanations/%s-a.jpg" %(os.path.dirname(fname),os.path.basename(fname))
    hole_node_path = "result/%s/hole-txt/%s.txt" %(os.path.dirname(fname),os.path.basename(fname))

    
    print("[LOADING] ",fname)
    #The node, edge and hole attributes
    all_nodes = []
    all_edges = []
    
    
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
    img = np.full((img_size, img_size, 3), 255,np.uint8)
    #Get all the number node coordinate
    for i in range (0,num_nodes):
        node = data_list.pop(0) #Pop out the node coordinate
        node = node.split()
        node.pop(0) #Pop out the node index  
        all_nodes.append((int(float (node[0])*(img_size-50)+25),int(float (node[1])*(img_size-50)+25))) #(X, Y)
       
    num_edges = int (data_list.pop(0)) #Pop out the number of edges 
    #Get all the edge
    for i in range (0,num_edges): 
        edge = data_list.pop(0) #Pop out the edge connection
        edge = edge.split()
        all_edges.append([int(edge[0]),int(edge[1])]) #(point 1, point 2)
        cv2.line(img, all_nodes[all_edges[i][0]], all_nodes[all_edges[i][1]],(1,0,56),2)
    data_f.close
    for i in range (0,num_nodes):
        cv2.circle(img, all_nodes[i], 8,(200,100,255),-1)

    #Save result Image
    img_c= img.copy()
    conf = [yolo_cfg_loc,img,confidence,threshold]
    img, boxes, idxs,s = yolo.runYOLOBoundingBoxes(conf)
    print("[INFO] Number of Detection Boxes: %s" %len(boxes))

    
    if len(boxes) == 0:
        print("\n[INFO] No Object In The Image.")
        with open(hole_node_path ,'w') as f:
            f.write("%s\n"%num_nodes)
            print("[INFO] Hole is not exsit." )
        f.close()
    else:
        
        print("[INFO] boxes' length: ", len(boxes))
        print("[INFO] idxs' shape: ", idxs.shape)
        mask = np.zeros((img_size+2,img_size+2), np.uint8)    
        
       
        for i in range(len(boxes)):
            x0=boxes[i][0]
            y0=boxes[i][1]
            w = boxes[i][2]
            h = boxes[i][3]
            
            x1=boxes[i][0]+w
            y1=boxes[i][1]+h
            w2 =int(x0+ w/2)
            h2 =int(y0+ h/2)
            print("[INFO] boxes ",i," size: ",(w, h))
            print("[INFO] center point:",(w2,h2),"center color:",img_c[w2,h2])
            print("[INFO] The Hole:",(img_c[h2,w2]==(255,255,255)).all(),"\n")  
            
            if ((img_c[h2,w2]==(255,255,255)).all())or((img_c[h2,w2]==(117,218,173)).all()):
                cv2.floodFill(img_c,mask,(w2,h2), (117,218,173), (0,0,0),(0,0,0),cv2.FLOODFILL_FIXED_RANGE)
    
        mask = np.zeros((img_size+2,img_size+2), np.uint8)   
        for x in range(1,img_size-1):
            cv2.floodFill(img_c,mask,(x,0), (255,255,255),(0,0,0),(0,0,0),cv2.FLOODFILL_FIXED_RANGE)
            cv2.floodFill(img_c,mask,(x,img_size-1), (255,255,255), (0,0,0),(0,0,0),cv2.FLOODFILL_FIXED_RANGE)
        mask = np.zeros((img_size+2,img_size+2), np.uint8)
        for y in range(1,img_size-1):
            cv2.floodFill(img_c,mask,(0,y), (255,255,255),(0,0,0),(0,0,0),cv2.FLOODFILL_FIXED_RANGE)
            cv2.floodFill(img_c,mask,(img_size-1,y), (255,255,255), (0,0,0),(0,0,0),cv2.FLOODFILL_FIXED_RANGE)
        
        cv2.imwrite(pre_image_path, img_c) #no need now.
        lower_hole=np.array((17,118,73))
        upper_hole=np.array([150,255,255])
        hole_mask=cv2.inRange(img_c,lower_hole,upper_hole)
        img_d = img.copy()
        img_hole = cv2.bitwise_and(img_d,img_d,mask=hole_mask)
    
        all_holes,_ = cv2.findContours(hole_mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
        area_min = int(img_size/ 4)
        tmp = [x for x in all_holes if not (cv2.contourArea(x) <= area_min)]      
        all_holes = sorted(tmp, key=cv2.contourArea)
        
        for i in range(len(boxes)):
            y0=boxes[i][1]
            x0=boxes[i][0]
            w = boxes[i][2]
            h = boxes[i][3]
            
            x1=boxes[i][0]+w
            y1=boxes[i][1]+h
            
            h2 =int(y0+ h/2)
            w2 =int(x0+ w/2)    
            cv2.circle(img_c,(w2,h2), 4,(0,0,255),-1)
            cv2.rectangle(img_c,(x0,y0),(x1,y1), (255,0,255),2)
            cv2.putText(img_c, str(i),(w2,h2), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 1, cv2.LINE_AA)
    
        for i in range (len(all_holes)):
            cv2.drawContours(img_hole,all_holes[i],-1,(255,255,255),5,cv2.LINE_AA)
        
        holes_nodes = []  #The nodes of hole 
        a = 0.0         #The return value of distance which between the nodes and hole in the image  
        d = -10.99       #The distance which between the nodes and hole
        
        with open(hole_node_path ,'w') as f:
            f.write("%s\n"%num_nodes)
            for i in range (len(all_holes)):
                holes_nodes = []
                for j in range (len(all_nodes)):
                    a = cv2.pointPolygonTest(all_holes[i],all_nodes[j],True) 
                    if (a > d):
                        holes_nodes.append(j)
                
                        cv2.circle(img_c, all_nodes[j], 15,(0,0,255),thickness = 2)
                        cv2.circle(img_c, all_nodes[j], 8,(0,255,255),-1)
                if holes_nodes:
                    f.write("%s\n"%(holes_nodes))
                    print("[OBJECT INFO] Hole %s:" %i ,holes_nodes)
        f.close()
        cv2.imwrite(hole_ana_path, img_c)        
    print("[DONE] Detection DONE.")



#Main program
yolo_cfg_loc = "yolo-hole" #the model path

#If u only want to detect one sensor network,uncomment below and comment #Sparse sersor network and #Uniform sersor network.
#Only detect one sensor network
'''
fname = 'Grouth/Uniform/n=1000d=15' #The path of the sersor network
yolo_hole_detection(fname,yolo_cfg_loc,confidence = 0.30,threshold =0.001)
print("[DONE] ALL DONE.")
'''

# GT sersor network
path = input("Input the Gruond Truth sensor network path:")
path  = path.split()
for i in range(0,len(path)):
    dirs = []
    dirs = os.listdir(path[i])
    print(dirs)
    for j in range(0,len(dirs)):
        fname = path[i] + dirs[j]
        yolo_hole_detection(fname,yolo_cfg_loc,confidence = 0.25,threshold =0.001)
        print(fname)

print("[DONE]ALL DONE.")




