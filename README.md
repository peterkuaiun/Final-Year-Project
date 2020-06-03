# Content
- Dataset  
    - Ground Truth Dataset
    - Force-Directed Dataset
    - YOLOv3 Hole Detection Model

- Installation requirements  
    - Library

- 4.2	Feature Extraction Methods
    - Graph Segmentation
    - Feature Transformation
    - Graph Segmentation and Feature Transformation with Specific Classification
    
 - Hole Detection in sensor network by CNN
    -Hole Detection in Ground truth sensor network by CNN
    -Hole Detection in Force-Directed algorithms sensor network by CNN
    
- 5.3	Performance Evaluation of Hole Detection in Sensor Network by Convolutional Neural Network 
    - Count Number of Hole
    - Calculate Sensitivity and Specificity of Hole Detection result

---

# Dataset
### Ground Truth Dataset  
All the dataset in our application is generated by CNCAHNetGenerator
There are some parameters can input, you can get a sensor networkafter **"Start Generator"**. Then click **"Export"** you will get a text file of the sensor network.  

CNCAHNetGenerator  
http://eric.lostcity-studio.com/system-design/cncahnetgenerator-cncah-network-generator/

### Force-Directed Dataset
The input of the force-directed algorithm is the ground truth sensor network. We used 10 force-directed algorithms to generate our experiment dataset. The format of the files is the same as ground truth.  

### YOLOv3 Hole Detection Model
If you want used Hole Detection in sensor network by CNN, you must download the Hole Detection Model and save it at "\HoleDetection_SensorNetwork_byCNN\yolo-hole".
The Hole Detection Model is trained by 40 Grouth Truth sensor network and each Feature Extraction Methods.

https://drive.google.com/file/d/1pIkYphKDOAy7VrYXzDHoeKjm5vykillp/view?usp=sharing




##### You can download the dataset below:
https://drive.google.com/file/d/1XRCJY0dodz932A2Kynlm3GJNu-cv2vdO/edit **(within Ground truth dataset)**  
https://drive.google.com/file/d/1q_f6r7ihGPq2pcnLhQLKZl1ynAXRENwQ/edit  
https://drive.google.com/file/d/1q1ykn7R_orQvvDplbiqQ2kXVIgJxGwd0/edit  
https://drive.google.com/file/d/1rCqSkBhN4yjBZCltMAfFcx_XLuaTKktH/view


    
---
# Installation requirements  
### Python 
Python 3.7 or later  
Offical website: https://www.python.org/

### OpenCV
OpenCV-python-4.2.0.32 or later  
Offical website: https://opencv.org/

**After installing Python and OpenCV, the program can run successfully.**

---

# 4.2	Feature Extraction Methods
## Graph Segmentation       

    FeatureExtruction-GS.py
    
This is a Python program that performing Feature Extraction Methods by Graph Segmentation which is for collecting the feature of holes in sensor networks.  
Input is a sensor network that include node coordinate and node connection.  
Output is the image and label of all the Hole object in sensor network by Graph Segmentation.

##### Command:  
    
    py FeatureExtruction-GS.py
    Input the sensor network path: [input_path] [input_path] ... [input_path]
    Input each sensor network type (Sparse input s; Uniform input u; Other input a): [s] [u] [a] ...[s]

##### Example:

    py FeatureExtruction-GS.py
    Input the sensor network path: n-data\Sparse\ n-data\Uniform\
    Input each sensor network type (Sparse input s; Uniform input u; Other input a): s u
    
## Feature Transformation       

    FeatureExtruction-FT.py
    
This is a Python program that performing Feature Extraction Methods by Feature Transformation which is for collecting the feature of holes in sensor networks.  
Input is a sensor network that include node coordinate and node connection.  
Output is the image and label of all the Hole object in sensor network by Feature Transformation.

##### Command:  
    
    py FeatureExtruction-FT.py
    Input the sensor network path: [input_path] [input_path] ... [input_path]
    Input each sensor network type (Sparse input s; Uniform input u; Other input a): [s] [u] [a] ...[s]

##### Example:

    py FeatureExtruction-FT.py
    Input the sensor network path: n-data\Sparse\ n-data\Uniform\
    Input each sensor network type (Sparse input s; Uniform input u; Other input a): s u

## Graph Segmentation and Feature Transformation with Specific Classification     

    FeatureExtruction-GS-FT-SC.py
    
This is a Python program that Feature Extraction Methods by Graph Segmentation and Feature Transformation with Specific Classification which is for collecting the feature of holes in sensor networks.  
Input is a sensor network that include node coordinate and node connection.  
Output is the image and label of all the Hole object in sensor network by Graph Segmentation and Feature Transformation with Specific Classification.

##### Command:  
    
    py FeatureExtruction-GS-FT-SC.py
    Input the sensor network path: [input_path] [input_path] ... [input_path]
    Input each sensor network type (Sparse input s; Uniform input u; Other input a): [s] [u] [a] ...[s]

##### Example:

    py FeatureExtruction-GS-FT-SC.py
    Input the sensor network path: n-data\Sparse\ n-data\Uniform\
    Input each sensor network type (Sparse input s; Uniform input u; Other input a): s u
    
# Hole Detection in sensor network by CNN
    If you want to use this program, you must download the Hole Detection Model first.
## Hole Detection in Ground truth sensor network by CNN
    
    hole-detection-byCNN_GT.py
This is a Python program that implement Convolutional Neural Network (CNN) for the hole detection in Ground truth sensor networks
Input is a sensor network that include node coordinate and node connection.
Output is the image of detected sensor network and a text file that include all the nodes of holes in the input sensor network.

##### Command:  
    
    py hole-detection-byCNN_GT.py
    Input the sensor network path: [input_path] [input_path] ... [input_path]

##### Example:

    py hole-detection-byCNN_GT.py
    Input the sensor network path: GroundTruth\Sparse\ GroundTruth\Uniform\
    
    
## Hole Detection in Force-Directed algorithms sensor network by CNN
    
    hole-detection-byCNN_FD.py
This is a Python program that implement Convolutional Neural Network (CNN) for the hole detection in Force-Directed algorithms sensor networks
Input is a sensor network that include node coordinate and node connection.
Output is the image of detected sensor network and a text file that include all the nodes of holes in the input sensor network.

##### Command:  
    
    py hole-detection-byCNN_FD.py
    Input the sensor network path: [input_path] [input_path] ... [input_path]

##### Example:

    py hole-detection-byCNN_FD.py
    Input the sensor network path: FD\Sparse\ FD\Uniform\
    
# 5.3	Performance Evaluation of Hole Detection in Sensor Network by Convolutional Neural Network 
## Count Number of Hole

    HoleNodeMatching_HoleDetectionCNN.py
This is a Python program for counting the number of hole in sensor network of experiment dataset.
Input is the output text file from **hole-detection-byCNN_TG.py OR hole-detection-byCNN_FD.py** that include all the nodes of holes
Output is the Sensitivity and Specificity of Hole Detection result in the input sensor network.


##### Command: 
    
    py HoleNodeMatching_HoleDetectionCNN.py
    Input the 2 path of detected hole node in sensor network and the result output path: [input_path] [input_path]

##### Example:

    py HoleNodeMatching_HoleDetectionCNN.py
    Input the 2 path of detected hole node in sensor network and the result output path: GroundTruth\Sparse\ GroundTruth\Uniform\


## Calculate Sensitivity and Specificity of Hole Detection result

    SensitivitySpecificity_HoleDetectionCNN.py
This program is for calculating the average of Sensitivity and Specificity in each number of node and average degrees in sensor network of experiment dataset.
Input is the output text file from **HoleNodeMatching_HoleDetectionCNN.py** that include the Sensitivity and Specificity of the sensor network.
Output is the average of Sensitivity and Specificity in each number of node and average degrees in the input sensor network.


##### Command:  
    
    py SensitivitySpecificity_HoleDetectionCNN.py
    Input the path of performance result in sensor network and the result output path: [input_path] [input_path]

##### Example:

    py SensitivitySpecificity_HoleDetectionCNN.py
    Input the path of performance result in sensor network and the result output path: GroundTruth\Sparse\ GroundTruth\Uniform\


    
    

