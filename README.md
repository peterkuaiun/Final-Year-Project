# Final-Year-Project
# Hole-Detection-in-Wireless-Sensor-Networks-A-Deep-Learning-Approach
Hole Detection in Sensor Network by Convolutional Neural Network
# # 

# The System of Hole Detection in Sensor Network by Convolutional Neural Network

# # 

# Content
- Dataset  
    - Ground Truth Dataset
    - Force-Directed Dataset  

- Installation requirements  
    - Library

- 4.2	Feature Extraction Methods
    - Graph Segmentation
    - Feature Transformation
    - Graph Segmentation and Feature Transformation with Specific Classification
    
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
    
This is a python program that performing Feature Extraction Methods by Graph Segmentation.  
Input is a sensor network that include node coordinate and node connection.  
Output is a hole-marked image after Contour Tracing Algorithm.

##### Command:  
    
    py FeatureExtruction-GS.py
    Input the sensor network path: [input_path] [input_path] ... [input_path]
    Input each sensor network type (Sparse input s; Uniform input u; Other input a): [s] [u] [a] ...[s]

##### Example:

    py FeatureExtruction-GS.py
    Input the sensor network path: n-data\Sparse\ n-data\Uniform\
    Input each sensor network type (Sparse input s; Uniform input u; Other input a): s u
    
    

