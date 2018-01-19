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
# Description: Spatial Filters
# 
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
from scipy.misc import imread
    

def spacial_filt_image(input_image, filter_type, size=3, plot_result=False, *args, **kwargs):
    output_image = None    
    if filter_type == 'uniform':
        ndimage.filters.uniform_filter(input_image,size=size, output=output_image)
    elif filter_type == 'median':
        ndimage.filters.median_filter(input_image,size=size, output=output_image)
    elif filter_type == 'minimum':
        ndimage.filters.minimum_filter(input_image,size=size, output=output_image)
    elif filter_type == 'maximum':
        ndimage.filters.maximum_filter(input_image,size=size, output=output_image)
    