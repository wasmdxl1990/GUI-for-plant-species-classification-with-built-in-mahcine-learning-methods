# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 01:23:06 2018

@author: DongdongMa
"""

import cv2
from PIL import Image
from skimage.measure import label, regionprops
import matplotlib.image as mpimg
from scipy import ndimage as ndi, misc
import numpy as np
import math
from skimage.morphology import closing
from skimage.morphology import disk
import imageio
DIR_INPUT = 'C:/Users/ma125/OneDrive - purdue.edu/2018 Fall/CS501/Project/' 

def seg_cor(file,thresh = 100):

    img = Image.open(file)
    fn = lambda x : 0 if x > thresh else 255
    r = img.convert('L').point(fn, mode='1')
    r.save(DIR_INPUT+'GUI/first.jpg')
    img1=np.array(r)
    Img=img1/255


    label_objects, nb_labels = ndi.label(Img)
    sizes = np.bincount(label_objects.ravel())
    mask_sizes = sizes > 20000
    mask_sizes[0] = 0
    coins_cleaned = mask_sizes[label_objects]
    Clean_Image=ndi.binary_closing(coins_cleaned, structure=np.ones((2,2))).astype(np.int)

    label_img1 = label(Clean_Image,neighbors=8,background=0)
    region1 = regionprops(label_img1, intensity_image=None, cache=True,)
    Rotate_degree=region1[0].orientation
    Rotate_degree1=Rotate_degree*360/math.pi/2
    rotate_img = r.rotate(-Rotate_degree1)
    rotate_img.save(DIR_INPUT+'GUI/second.jpg')
    path=DIR_INPUT+'GUI/second.jpg'
    Imgtest=mpimg.imread(path)
    Imgtest1=Imgtest/255
    label_objects, nb_labels = ndi.label(Imgtest1)
    sizes = np.bincount(label_objects.ravel())
    mask_sizes = sizes > 20000
    mask_sizes[0] = 0
    coins_cleaned = mask_sizes[label_objects]
    Clean_Image=ndi.binary_closing(coins_cleaned, structure=np.ones((2,2))).astype(np.int)
    selem = disk(5)
    closed = closing(Clean_Image, selem)
    closed1 = ndi.binary_fill_holes(closed)
    closed1 = closed1.astype(np.uint8)  #convert to an unsigned byte
    closed1 *= 255
    imageio.imwrite(DIR_INPUT+'GUI/third.jpg', closed1)


#file = 'C:/Users/Dong/OneDrive - purdue.edu/2018 Fall/CS501/Project/GUI/capture.jpg'
#seg_cor(file)












