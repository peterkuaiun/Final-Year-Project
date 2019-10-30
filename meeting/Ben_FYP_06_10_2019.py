"""
Created on Sun Oct  6 16:50:24 2019
2019_UM_FST_CPS_FYP_Hole Detection in Sensor Network Project

FYP_06_10_2019
@author:     Ng Kim Hou
@Student ID: DB625369
@Description: 
1. Test input an image convert to bitmap
2. Find all the edges 
   
"""
from PIL import Image

#Input the image and the image convert RGB mode 
img = Image.open("test_1.png").convert('RGB')

#Copy to the result image
b_img = img.copy()

#load the image
pixels = b_img.load()

#useing the black pixels to find the edges 
for x in range(b_img.height-1):
    for y in range(b_img.width-1):
        
        #If the pixels is black, change the color to red.
        if (pixels[x, y] != (255, 255, 255)):
            pixels[x, y] = (255, 0, 0) 


print('DONE')

#Save the image as bitmap
b_img.save("test1.bmp")

#Show the result
img.show()
b_img.show()
