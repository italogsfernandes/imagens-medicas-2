# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# FEDERAL UNIVERSITY OF UBERLANDIA
# Faculty of Electrical Engineering
# Biomedical Engineering Lab
# ------------------------------------------------------------------------------
# Author: Italo Gustavo Sampaio Fernandes
# Contact: italogsfernandes@gmail.com
# Git: www.github.com/italogfernandes
# ------------------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------------------
import sys
# ------------------------------------------------------------------------------

import numpy as np
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
from scipy.misc import imread

def average_filter(input_image, window_size, plot_result=False):
    """
    [outputImage] = average_filter(inputImage, windowSize, plotResult)
    Parameters
    ----------
    input_image : input image (nparray)
    window_size : mask size
    plot_result: True or False. Plot input and output images with respective
    histogram
    
    Returns
    -------
        output_image : output image (nparray)
    """
    # Using processing toolbox
    output_image = ndimage.uniform_filter(input_image,size=window_size)
       
    if plot_result:
        plt.figure()
        plt.subplot(1,2,1)
        plt.imshow(input_image, cmap=plt.cm.gray)
        plt.title('Input Image')
        plt.subplot(1,2,2)
        plt.imshow(output_image, cmap=plt.cm.gray)
        plt.title('Output Image')
        plt.show()
    return output_image



def test():
    size = None
    file_path = None    
    selected_image = None
    while True:
        print('-------------------------------')
        print('Average Filter')
        print('-------------------------------')
        print('Menu')
        print('-------------------------------')
        print('image: example.png - load a file')
        print('s4 - set the window size to 4')
        print('go - executa')
        print('q - Quit')
        print('-------------------------------')
        
        if sys.version_info.major == 2:
            str_key = raw_input()
        else:
            str_key = input()
        
        if str_key == 'q':
            break
        elif str_key[0] == 's':
            size = int(str_key[1:])
            print("%d selected as window size" % size)
        elif str_key.split()[0].startswith('image'):
            file_path = str_key.split()[1]
            try:
                selected_image = imread(file_path)
                print("Imagem %s carregada" % file_path)
            except:
                print("Ocorreu algum erro...\n%s"  % sys.exc_info()[0])
        elif str_key == 'go':
            if not size is None and not selected_image is None:
                average_filter(selected_image,size,True)
            else:
                print("Carregue uma imagem e um tamanho de janela")
                
if __name__ == '__main__':  # if we're running file directly and not importing it
   test()
