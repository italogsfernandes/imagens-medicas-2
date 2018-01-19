# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# FEDERAL UNIVERSITY OF UBERLANDIA
# Faculty of Electrical Engineering
# Biomedical Engineering Lab
# ------------------------------------------------------------------------------
# Author: Italo Gustavo Sampaio Fernandes
# Contact: italogsfernandes@gmail.com
# Git: www.github.com/italogfernandes
# This project is based on: https://github.com/ronaldosena/imagens-medicas-2
# Please give the credits to ronaldo sena.
# ------------------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# ------------------------------------------------------------------------------
from scipy.misc import imread
import matplotlib.image as mpimg
import scipy.ndimage as ndimage
from matlab_fspecial import fspecial

# First part
files_folder = '../../datasets/' # Caminho para a pasta onde estao as imagens
file_names = ('arteriaBMP.bmp','blood0.PNG','blood1.PNG','pe.jpg')
in_images = [imread(files_folder+image_name) for image_name in file_names ]
out_images = [None] * len(file_names)
brightness = 100
mask_sizes = (3,7,25)
kernels = []

for mask_size in mask_sizes:
    kernels.append(fspecial('average',mask_size))

# for in_image in in_images:
for i in range(len(file_names)):
    in_image = in_images[i] 
    o1 = in_image + brightness
    o1[in_image > (255 - brightness)] = 255 
    o2 = in_image - brightness
    o2[in_image < (0 + brightness)] = 0
    out_images[i] = [o1, o2]
    
    plt.figure()
    
    plt.subplot(2,len(mask_sizes)+1,1)    
    plt.imshow(in_image, cmap=plt.cm.gray)
    plt.title('Original')
    
    plt.subplot(2,len(mask_sizes)+1,len(mask_sizes)+2)
    plt.hist(in_image.ravel(),256,[0,256])
    plt.title('Histograma original')

    out_images_line = []
    for j in range(len(mask_sizes)):
        out_image = ndimage.uniform_filter(in_image,size=mask_sizes[j])
        #out_image = ndimage.correlate(in_image,kernels[j])
        out_images_line.append(out_image)

        plt.subplot(2, len(mask_sizes)+1, j+2)
        plt.imshow(out_image, cmap=plt.cm.gray)
        plt.title('Mascara de %dx%d' % (mask_sizes[j], mask_sizes[j]))
        
        plt.subplot(2, len(mask_sizes)+1,j+len(mask_sizes)+3)
        plt.hist(out_image.ravel(),256,[0,256])
        plt.title('Histograma com mascara de %dx%d' % (mask_sizes[j], mask_sizes[j]))
        
    out_images.append(out_images_line)
    

plt.show()
