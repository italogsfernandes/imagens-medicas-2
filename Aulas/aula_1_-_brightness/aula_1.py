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
# First part
files_folder = '../../datasets/' # Caminho para a pasta onde estao as imagens
file_names = ('arteriaBMP.bmp','blood0.PNG','blood1.PNG','pe.jpg')
in_images = [imread(files_folder+image_name) for image_name in file_names ]
out_images = [None] * len(file_names)
brightness = 100

# for in_image in in_images:
for i in range(len(file_names)):
    in_image = in_images[i] 
    o1 = in_image + brightness
    o1[in_image > (255 - brightness)] = 255 
    o2 = in_image - brightness
    o2[in_image < (0 + brightness)] = 0
    #o1 = np.clip((in_image.astype(np.float64) + brightness),0,255).astype(in_image.dtype)
    #o2 = np.clip((in_image.astype(np.float64) - brightness),0,255).astype(in_image.dtype) 
    out_images[i] = [o1, o2]
    
    plt.figure()
    
    plt.subplot(2,3,1)
    plt.imshow(in_image, cmap=plt.cm.gray)
    plt.title('Original')
    plt.subplot(2,3,4)
    plt.hist(in_image.ravel(),256,[0,256])
    plt.title('Histograma original')
    
    plt.subplot(2,3,2)
    plt.imshow(out_images[i][0], cmap=plt.cm.gray)
    plt.title('Brilho aumentado de %d' % (brightness))
    plt.subplot(2,3,5)
    plt.hist(out_images[i][0].ravel(),256,[0,256])
    plt.title('Histograma do brilho aumentado de %d' % (brightness))
        
    plt.subplot(2,3,3)
    plt.imshow(out_images[i][1], cmap=plt.cm.gray)
    plt.title('Brilho diminuido de %d' % (brightness))
    plt.subplot(2,3,6)
    plt.hist(out_images[i][1].ravel(),256,[0,256])
    plt.title('Histograma do brilho diminuido de %d' % (brightness))


plt.show()
