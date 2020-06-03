#!/usr/bin/python

import numpy as np

import time
import cv2 as cv
import os
classes_name = ['4-nodes-hole','5-nodes-hole','6-nodes-hole','simple-polygon-hole']

def runYOLOBoundingBoxes(args):
    netsize = 0
    # load my fish class labels that my YOLO model was trained on
    labelsPath = os.path.sep.join([args[0], os.path.basename(args[0] )+".names"])
    weightsPath = os.path.sep.join([args[0],  os.path.basename(args[0])+".weights"])
    configPath = os.path.sep.join([args[0],  os.path.basename(args[0])+".cfg"])
    print("[LOAD] weight file.",weightsPath)
    print("[LOAD] config file.",configPath)
   # print(os.path.basename(args[0] ))
    #LABELS = open(labelsPath).read().split("\n")
    print("[LOAD] labels file.",labelsPath)

    # initialize a list of colors to represent each possible class label
    np.random.seed(0)
    '''
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
        dtype="uint8")
    print("The classes colors:\n",COLORS)
    COLORS = np.array([255, 0, 0], dtype="uint8")
    '''
    
    
    # derive the paths to the YOLO weights and model configuration
    #weightsPath = os.path.sep.join([args[0], "yolov3.weights"])
    #configPath = os.path.sep.join([args[0], "yolov3.cfg"])

    # load my YOLO object detector trained on my fish dataset (1 class)
    print("[INFO] loading YOLO from disk ...")
    net = cv.dnn.readNetFromDarknet(configPath, weightsPath)

    # load input image and grab its spatial dimensions
    image = args[1]
    print(image.shape[:2])
    (H, W) = image.shape[:2]

    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    #print("1.ln:" ,ln)
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    #print("2.ln:" ,ln)
    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    # NOTE: (608, 608) is my YOLO input image size. However, using 
    # (416, 416) results in much accutate result. Pretty interesting.

    netsize = int(H/32 +1) * 32 
    if(H>4000):
        netsize = int(4000/32+1)*32
    print(netsize)
    blob = cv.dnn.blobFromImage(image, 1 / 255.0, (netsize, netsize),swapRB=True, crop=False)
    
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    #print("layerOutputs:" ,len(layerOutputs))
    end = time.time()

    # show execution time information of YOLO
    print("[INFO] YOLO took {:.6f} seconds.".format(end - start))

    # initialize out lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            #print(scores)
            #print(classID)
            # filter out weak predictions by ensuring the detected
            # probability is greater then the minimum probability
            if confidence > args[2]:
                #print(args[2])
                print("[PREDICTION] %f %s" %((confidence*100),classes_name[classID]))
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # left corner of the bounding box
                x = int(centerX - (width / 2)-10)
                y = int(centerY - (height / 2)-10)
                if x < 0:
                    x=0
                if y < 0:
                    y=0
                
                # update out list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width)+10, int(height)+10])
                
                confidences.append(float(confidence))
                classIDs.append(classID)
                
    # apply non-maxima suppression to suppress weark and overlapping bounding boxes
    
    if boxes == 0:
        idxs = 0
    else:
        #boxes[boxes< 0] = 0
        idxs = cv.dnn.NMSBoxes(boxes, confidences, args[2],args[3])

       
     
    #boxes[boxes< 0] = 0
    return image, boxes, idxs, classIDs
