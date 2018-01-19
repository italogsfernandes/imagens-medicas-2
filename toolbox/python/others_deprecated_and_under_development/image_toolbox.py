# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 21:50:03 2018

@author: italo
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
from scipy.misc import imread    
from skimage import exposure

def equalize(input_image, plot_result=False, *args, **kwargs):
    output_image = exposure.equalize_hist(input_image)
    return output_image
    