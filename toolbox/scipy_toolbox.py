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
# Description: Scipy image toolbox
#   Based on: 
#   http://www.scipy-lectures.org/advanced/image_processing/index.html
#   and
#   TODO: https://docs.scipy.org/doc/scipy/reference/tutorial/ndimage.html
# ------------------------------------------------------------------------------
from scipy import misc # Opening and clossing
import matplotlib.pyplot as plt # Showing the images
import numpy as np # Image manipulation as nparray
from scipy import ndimage # Gaussian filter
# ------------------------------------------------------------------------------
## Saving and reading images, basics
# ------------------------------------------------------------------------------
def save_image(input_image,name=None,extension='.png',folder=None):
    complete_file_name = name + extension
    if not folder is None:
        complete_file_name = folder + complete_file_name   
    misc.imsave(complete_file_name, input_image) # uses the Image module (PIL)

def read_image(name,extension='.png',folder=None):
    """
    Reads a image from file.
    Other options
    -------------
    Opening raw files
    >>> face_from_raw = np.fromfile('face.raw', dtype=np.uint8)
    >>> face_from_raw.shape = (768, 1024, 3)
    Need to know the shape and dtype of the image (how to separate data bytes).
    
    For large data, use np.memmap for memory mapping:
    >>> face_memmap = np.memmap('face.raw', dtype=np.uint8, shape=(768, 1024, 3))
    (data are read from the file, and not loaded into memory)
   
    Working on a list of image files
    >> from glob import glob
    >> filelist = glob('random*.png')
    """
    complete_file_name = name + extension
    if not folder is None:
       complete_file_name = folder + complete_file_name   
    
    output_image = misc.imread(complete_file_name)
    return output_image

# ------------------------------------------------------------------------------
## Showing images
# ------------------------------------------------------------------------------
def show_image(input_image,title=None, colorbar=False):
    if input_image.dtype == np.float64:
        min_value = min(input_image.ravel())
        max_value = max(input_image.ravel())
    else:
        min_value = np.iinfo(input_image.dtype).min
        max_value = np.iinfo(input_image.dtype).max    
    im = plt.imshow(input_image, cmap=plt.cm.gray,clim=(min_value, max_value))
    if colorbar:
        plt.colorbar(orientation='vertical')
    if not title is None:
        plt.title(title)
    return im

def show_hist(input_image,title=None):
    #plt.hist(input_image.ravel(), bins=256, range=(0, 255), normed=True,
    #        histtype='stepfilled')
    #plt.hist(input_image.ravel(), bins=256, range=(0, 255))
    if input_image.dtype == np.float64:
        min_value = min(input_image.ravel())
        max_value = max(input_image.ravel())
    else:
        min_value = np.iinfo(input_image.dtype).min
        max_value = np.iinfo(input_image.dtype).max  
    plt.hist(input_image.ravel(), bins=256, range=(min_value, max_value), normed=True)
    if not title is None:
        plt.title(title)

def show_image_and_hist(input_image,im_title=None, hist_title=None,colorbar=True):
    plt.subplot(2,1,1)
    im = show_image(input_image,im_title)
    plt.subplot(2,1,2)
    show_hist(input_image,hist_title)
    if colorbar:
        plt.colorbar(im, orientation='horizontal')

def show_images_and_hists(input_images,titles=[],hist_titles=[],colorbar=True):
    qnt = len(input_images)

    if not titles == []  and hist_titles == []:
        hist_titles = ['Histogram of ' + title for title in titles]  
        
    for i in range(qnt):
        plt.subplot(2,qnt,i+1)
        im = show_image(input_images[i],titles[i] if not titles == [] else None)
        plt.subplot(2,qnt,qnt+i+1)
        show_hist(input_images[i],hist_titles[i] if not hist_titles == [] else None)
        if colorbar:
            plt.colorbar(im, orientation='horizontal')
        
# ------------------------------------------------------------------------------
## Filtering images
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
## Spatial Filtering
# ------------------------------------------------------------------------------
def gaussian_filter(input_image, sigma=3, show_result=False):    
    blurred_image = ndimage.gaussian_filter(input_image, sigma=sigma)
    if show_result:
        show_images_and_hists([input_image,blurred_image],['Input', 'Gaussian Filter'])
    return blurred_image
    
def uniform_filter(input_image, size=3, show_result=False):
    local_mean = ndimage.uniform_filter(input_image, size)
    if show_result:
        show_images_and_hists([input_image,local_mean],['Input', 'Uniform Filter'])
    return local_mean
    
def sharpenning_filter(input_image, alpha = 30, filter_sigma=1,show_result=False):
    filter_blurred_f = ndimage.gaussian_filter(input_image, filter_sigma)
    sharpened = input_image + alpha * (input_image - filter_blurred_f)
    if show_result:
        show_images_and_hists([input_image,sharpened],['Input', 'Sharpened'])
    return sharpened

# ------------------------------------------------------------------------------
## TODO: Denoising
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
## TODO: Mathematical morphology (Erosion, Dilation, )
# ------------------------------------------------------------------------------
# TODO: Erosion removes objects smaller than the structure
# TODO: Dilation: maximum filter
# TODO: Opening: erosion + dilation:
#       # Opening removes small objects
#       # Opening can also smooth corners
#       # Application: remove noise:

# ------------------------------------------------------------------------------
## TODO: Spectral Filtering
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
## TODO: Spatial Filtering
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
## TODO: Spatial Filtering
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
## TODO: Feature Extraction
# TODO: 2.6.5.1. Edge detection
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# TODO: Segmentation
# Simple Segmentation
# Median segimentation.
# Segmentation+opening/closing
# Segimentaton+reconstruction
# Histogram-based segmentation (no spatial information)
# Use mathematical morphology to clean up the result:
#   Remove small black points
#   Remove small white points
# Check that reconstruction operations (erosion + propagation) produce a better result than opening/closing
# Check how a first denoising step (e.g. with a median filter) modifies the histogram, and check that the resulting histogram-based segmentation is more accurate.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Measuring objects properties: ndimage.measurements
# TODO: Analysis of connected components
# Other spatial measures: ndimage.center_of_mass, ndimage.maximum_position, etc.
# ------------------------------------------------------------------------------


def test():
    print("Example")
    def save_image_example():
        f = misc.face()
        save_image(f,'face') # uses the Image module (PIL)
    
    def show_image_example():
        f = misc.face()
        show_image(f,'face') # uses the Image module (PIL)        
     
    def read_image_example():
        my_image = read_image('blood1','.PNG','../datasets/')
        show_image(my_image)
    
    def show_hist_example():
        my_image = read_image('blood1','.PNG','../datasets/')
        show_hist(my_image)
        
    def show_image_and_hist_example():
        my_image = read_image('blood1','.PNG','../datasets/')
        show_image_and_hist(my_image,'Blood', 'Histogram of Blood')
    
    def gaussian_filter_example():
        my_image = read_image('blood1','.PNG','../datasets/')
        gaussian_filter(my_image,show_result=True)
    
    def uniform_filter_example():
        my_image = read_image('blood1','.PNG','../datasets/')        
        uniform_filter(my_image,size=11,show_result=True)
        
    def sharpenning_filter_example():        
        face = misc.face(gray=True).astype(np.float64)
        blurred_f = ndimage.gaussian_filter(face, 3)
        sharpenning_filter(blurred_f,alpha=30,filter_sigma=1,show_result=True)
                
    def denoising_example():
        """    
        2.6.4.3. Denoising    
        A Gaussian filter smoothes the noise out… and the edges as well:
        Most local linear isotropic filters blur the image (ndimage.uniform_filter)
        A median filter preserves better the edges:
        Median filter: better result for straight boundaries (low curvature):
        Other rank filter: ndimage.maximum_filter, ndimage.percentile_filter
        Other local non-linear filters: Wiener (scipy.signal.wiener), etc.
        """
        # TODO: Testar estes todos amanha e fazer comparativo, olhar no site
        pass
    
    
    #save_image_example()
    #show_image_example()
    #read_image_example()
    #show_hist_example()
    #show_image_and_hist_example()
    #gaussian_filter_example()
    #uniform_filter_example()    
    #sharpenning_filter_example()    
    #denoising_example()    
    plt.show()
    
if __name__ == '__main__':  # if we're running file directly and not importing it
   test()
     
       
  
