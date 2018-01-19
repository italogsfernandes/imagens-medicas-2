# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# FEDERAL UNIVERSITY OF UBERLANDIA
# Faculty of Electrical Engineering
# Biomedical Engineering Lab
# ------------------------------------------------------------------------------
# This file author: Italo Gustavo Sampaio Fernandes
# Contact: italogsfernandes@gmail.com
# Git: www.github.com/italogfernandes
# Base Author:  Ronaldo Sena
# ronaldo.sena@outlook.com
#   Use it as you please. If you meet him some day, and you think
#   this stuff was helpful, you can buy him a beer
#   Shout out to professor Ana Claudia, for the inspiring code
# ------------------------------------------------------------------------------
# Description:
# 
#   Ideal high pass filter. Takes in an image and a mask size and
#   oupts the filtered image in same type as original one
# 
#   [outputImage] = idealHighPass(inputImage, radius, plotResult) 
#   
#   Parameters
#       inputImage: Input image (any type)
#       noiseType: Select one of
#               'Uniform'
#               'Gaussian'
#               'Rayleight'
#               'Exponential'
#               'Gamma'
#               'SaltAndPepper'
#       par: Optional. Cell array with noise specific parameters
#       plotResult: Optional. 'yes' or 'no'. Plot input and output images with
#       respective frequency spectrogram
# 
#   Outputs
#       outputImage: output image (same type as inputImage)
#
#   Use example:
#       Insert 2# of noise in the image, (1# salt and 1# pepper)
#          outputImage = insertNoise(inputImage, 'SaltAndPepper', 'yes',{0.01});
# 
#       By default, insert 10# of noise in the image, (5# salt and 5# pepper)
#          outputImage = insertNoise(inputImage, 'SaltAndPepper');
#
# ------------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread

def insert_uniform_noise(input_image,low=0,high=80):
    return (input_image + np.random.uniform(low,high,input_image.shape)).astype(input_image.dtype)
    
def insert_gaussian_noise(input_image, mean=5, std=30):
    return (input_image + np.random.normal(mean,std,input_image.shape)).astype(input_image.dtype)

def insert_rayleight_noise(input_image, scale=20):
    return (input_image + np.random.rayleigh(scale,input_image.shape)).astype(input_image.dtype)
      
def insert_exponential_noise(input_image, scale=5):
    return (input_image + np.random.exponential(scale,input_image.shape)).astype(input_image.dtype)

def insert_gamma_noise(input_image, shape=1, scale=8):
    return (input_image + np.random.gamma(shape,scale,input_image.shape)).astype(input_image.dtype)

def insert_salt_and_pepper_noise(input_image,s_vs_p=0.5,amount=0.004,
                                 max_image_value=255):
    output_image = np.copy(input_image)
    # Salt mode
    num_salt = np.ceil(amount * input_image.size * s_vs_p)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in input_image.shape]
    output_image[coords] = max_image_value    
    # Pepper mode
    num_pepper = np.ceil(amount* input_image.size * (1. - s_vs_p))
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in input_image.shape]
    output_image[coords] = 0
    return (output_image).astype(input_image.dtype)

def insert_noise(input_image, noise_type, plot_result=False, *args, **kwargs):
    if noise_type == 'uniform':
        output_image = insert_uniform_noise(input_image,*args, **kwargs)
    elif noise_type == 'gaussian':
        output_image = insert_gaussian_noise(input_image,*args,**kwargs) 
    elif noise_type == 'rayleight':
        output_image = insert_rayleight_noise(input_image,*args,**kwargs) 
    elif noise_type == 'exponential':
        output_image = insert_exponential_noise(input_image,*args,**kwargs) 
    elif noise_type == 'gamma':
        output_image = insert_gamma_noise(input_image,*args,**kwargs) 
    elif noise_type == 'salt_and_pepper':
        output_image = insert_salt_and_pepper_noise(input_image,*args,**kwargs) 
       
    if plot_result:
        plt.figure()
        plt.subplot(2,2,1)
        plt.imshow(input_image, cmap=plt.cm.gray)
        plt.title('Input Image')
        plt.subplot(2,2,3)        
        plt.hist(input_image.ravel(),256)#,[0,256])
        plt.title('Input Histogram')
        
        plt.subplot(2,2,2)
        plt.imshow(output_image, cmap=plt.cm.gray)
        plt.title('Output Image - %s%s - %s - %s' % ("Noise: ", noise_type,
                                              str(args), str(kwargs)))
        plt.subplot(2,2,4)
        plt.hist(output_image.ravel(),256)#[0,256])
        plt.title('Output Histogram')
    return output_image
            
def test():
    file_path = '../datasets/blood1.PNG'   
    selected_image = imread(file_path)
    #selected_image = np.ones((100,100),dtype=np.uint8)*127
    
    #               'Uniform'
    #               'Gaussian'
    #               'Rayleight'
    #               'Exponential'
    #               'Gamma'
    #               'SaltAndPepper'
    uniform = insert_noise(selected_image,'uniform', True, low=0,high=80)
    gaussian = insert_noise(selected_image,'gaussian', True, mean=5, std=30)
    rayleight = insert_noise(selected_image,'rayleight', True, scale=20)
    exponential = insert_noise(selected_image,'exponential', True, scale=5)
    gamma = insert_noise(selected_image,'gamma', True, shape=1, scale=8)
    salt_and_pepper = insert_noise(selected_image,'salt_and_pepper', True,
                                   s_vs_p=0.5,amount=0.04,max_image_value=255)
    plt.show()
              
if __name__ == '__main__':  # if we're running file directly and not importing it
   test()
     
       
       
       
       
       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        