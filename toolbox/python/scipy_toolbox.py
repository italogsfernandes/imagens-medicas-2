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

def median_filter(input_image, size=3, show_result=False):
    local_median = ndimage.median_filter(input_image, size)
    if show_result:
        show_images_and_hists([input_image,local_median],['Input', 'Median Filter'])
    return local_median
    
def sharpenning_filter(input_image, alpha = 30, filter_sigma=1,show_result=False):
    filter_blurred_f = ndimage.gaussian_filter(input_image, filter_sigma)
    sharpened = input_image + alpha * (input_image - filter_blurred_f)
    if show_result:
        show_images_and_hists([input_image,sharpened],['Input', 'Sharpened'])
    return sharpened

# ------------------------------------------------------------------------------
## Inserting Noise
# ------------------------------------------------------------------------------
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

def insert_salt_and_pepper_noise(input_image,amount=0.004,s_vs_p=0.5):
    if input_image.dtype == np.float64:
        min_value = min(input_image.ravel())
        max_value = max(input_image.ravel())
    else:
        min_value = np.iinfo(input_image.dtype).min
        max_value = np.iinfo(input_image.dtype).max    
        
    output_image = np.copy(input_image)
    # Salt mode
    num_salt = np.ceil(amount * input_image.size * s_vs_p)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in input_image.shape]
    output_image[coords] = max_value    
    # Pepper mode
    num_pepper = np.ceil(amount* input_image.size * (1. - s_vs_p))
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in input_image.shape]
    output_image[coords] = min_value
    return (output_image).astype(input_image.dtype)

def insert_noise(input_image, noise_type, show_result=False, *args, **kwargs):
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
       
    if show_result:
        show_images_and_hists([input_image,output_image],
                              titles=['Input',
                              'Output Image - %s%s\n%s - %s' % ("Noise: ", noise_type,
                                              str(args), str(kwargs))],colorbar=True)
    return output_image

# ------------------------------------------------------------------------------
## Feature Extraction
# 2.6.5.1. Edge detection
# ------------------------------------------------------------------------------
def edge_detection(input_image,show_result=False):
    sx = ndimage.sobel(input_image, axis=0, mode='constant')
    sy = ndimage.sobel(input_image, axis=1, mode='constant')
    sob = np.hypot(sx, sy)
    if show_result:
        show_images_and_hists([input_image,sob], titles=['Input','Sobel'],
                              colorbar=True)
    return sob

# ------------------------------------------------------------------------------
# TODO: Segmentation
# Simple Segmentation
# Median Segmentation.
# Segmentation+opening/closing
# Segimentaton+reconstruction
# Histogram-based segmentation (no spatial information)
# Use mathematical morphology to clean up the result:
#   Remove small black points
#   Remove small white points
# Check that reconstruction operations (erosion + propagation) produce a better result than opening/closing
# Check how a first denoising step (e.g. with a median filter) modifies the histogram, and check that the resulting histogram-based segmentation is more accurate.
# ------------------------------------------------------------------------------

def simple_segmentation(input_image, show_result=False):
    """Histogram-based segmentation (no spatial information)"""
    #hist, bin_edges = np.histogram(img, bins=60)
    #bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])
    binary_img = input_image > np.mean(input_image)
    if show_result:
        show_images_and_hists([input_image, binary_img.astype(float)],
                               titles=['Input','Segmentation - %.2f' % (np.mean(input_image))],
                              colorbar=True)
    return binary_img
    
def openning_clossing_clear(binary_img,size=None, show_result=False):
    if size is None:    
        # Remove small white regions
        open_img = ndimage.binary_opening(binary_img)
        # Remove small black hole
        close_img = ndimage.binary_closing(open_img)
    else:
        # Remove small white regions
        open_img = ndimage.binary_opening(binary_img,structure=np.ones((size,size)))
        # Remove small black hole
        close_img = ndimage.binary_closing(open_img,structure=np.ones((size,size)))        
    if show_result:
        show_images_and_hists([binary_img,close_img], titles=['Input','Clear'],
                              colorbar=True)
    return close_img
      
def reconstruct_clear(binary_img,size=None,show_result=False):
    if size is None:    
        eroded_img = ndimage.binary_erosion(binary_img)
        reconstruct_img = ndimage.binary_propagation(eroded_img,mask=binary_img)
        tmp = np.logical_not(reconstruct_img)
        eroded_tmp = ndimage.binary_erosion(tmp)
        reconstruct_final = np.logical_not(ndimage.binary_propagation(eroded_tmp, mask=tmp))
    else:
        eroded_img = ndimage.binary_erosion(binary_img,structure=np.ones((size,size)))        
        reconstruct_img = ndimage.binary_propagation(eroded_img, structure=np.ones((size,size)), mask=binary_img)
        tmp = np.logical_not(reconstruct_img)
        eroded_tmp = ndimage.binary_erosion(tmp,structure=np.ones((size,size)))
        reconstruct_final = np.logical_not(ndimage.binary_propagation(eroded_tmp,structure=np.ones((size,size)), mask=tmp))
    if show_result:
        show_images_and_hists([binary_img,reconstruct_final], titles=['Input','Clear'],
                              colorbar=True)
    return reconstruct_final
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
    
    def insert_noise_example():
        selected_image = np.ones((100,100),dtype=np.uint8)*127
        plt.figure()        
        uniform = insert_noise(selected_image,'uniform', True, low=-40,high=40)
        plt.figure()        
        gaussian = insert_noise(selected_image,'gaussian', True, mean=0, std=30)
        plt.figure()
        rayleight = insert_noise(selected_image,'rayleight', True, scale=20)
        plt.figure()
        exponential = insert_noise(selected_image,'exponential', True, scale=5)
        plt.figure()
        gamma = insert_noise(selected_image,'gamma', True, shape=1, scale=8)
        plt.figure()
        salt_and_pepper = insert_noise(selected_image,'salt_and_pepper', True,
                                       s_vs_p=0.5,amount=0.5)
        
    def denoising_example():
        """    
        2.6.4.3. Denoising    
        """
        sr = False
        f = misc.face(gray=True)#.astype(np.float64)
        # Noisy face
        if sr:
            plt.figure()
        noisy = insert_noise(f,'uniform',show_result=sr,low=-30,high=30)        
        # A Gaussian filter smoothes the noise out… and the edges as well:        
        if sr:
            plt.figure()        
        gauss_denoised = gaussian_filter(noisy, sigma=2, show_result=sr)
        # Most local linear isotropic filters blur the image (ndimage.uniform_filter)        
        if sr:
            plt.figure()        
        uniform_denoised = uniform_filter(noisy,size=11,show_result=sr)
        # A median filter preserves better the edges:
        if sr:
            plt.figure()
        med_denoised = median_filter(noisy, size=3,show_result=sr)    
        
        if not sr:
            show_images_and_hists([f,noisy,gauss_denoised,uniform_denoised,
                                   med_denoised],
                                   ['original','noisy','gauss','uniform','median'])
            
    def denoising_example2():
        # Median filter: better result for straight boundaries (low curvature):
        im = np.zeros((20, 20))
        im[5:-5, 5:-5] = 1
        im = ndimage.distance_transform_bf(im)
        im_noise = im + 0.2 * np.random.randn(*im.shape)      
        im_med =  ndimage.median_filter(im_noise,3)
        plt.figure()        
        show_images_and_hists([im,im_noise,im_med],
                               ['original','noisy','med'])
        
    def denoising_example3():
        # Other rank filter: ndimage.maximun_filter, ndimage.percentile_filter
        im = np.zeros((20, 20))
        im[5:-5, 5:-5] = 1
        im = ndimage.distance_transform_bf(im)
        im_noise = im + 0.2 * np.random.randn(*im.shape)      
        im_max =  ndimage.maximum_filter(im_noise,3)
        im_p25 =  ndimage.percentile_filter(im_noise,25,3) 
        im_p50 =  ndimage.percentile_filter(im_noise,50,3)
        im_p75 =  ndimage.percentile_filter(im_noise,75,3)
        plt.figure()        
        show_images_and_hists([im,im_noise,im_max],
                               ['original','noisy','max'])
        plt.figure()    
        show_images_and_hists([im,im_noise,im_p25,im_p50,im_p75],
                               ['original','noisy','25%','50%','75%'])
        # TODO: Other local non-linear filters: Wiener (scipy.signal.wiener), etc.
        # TODO: Execise
    
    def erosion_example():
        el = ndimage.generate_binary_structure(2, 1)
        a = np.zeros((7,7), dtype=np.uint8)
        a[1:6, 2:5] = 1
        
        a_3 = ndimage.binary_erosion(a).astype(a.dtype)

        #Erosion removes objects smaller than the structure
        a_5 = ndimage.binary_erosion(a, structure=np.ones((5,5))).astype(a.dtype)
        plt.figure()    
        show_images_and_hists([a*255,a_3*255,a_5*255])
        
    def dilatation_example():
        a = np.zeros((5, 5))
        a[2, 2] = 1
        a_3 = ndimage.binary_dilation(a,structure=np.ones((3,3))).astype(a.dtype)
        a_4 = ndimage.binary_dilation(a,structure=np.ones((4,4))).astype(a.dtype)
        plt.figure()    
        show_images_and_hists([a*255,a_3*255,a_4*255])
        # Also work for gray values
        im = np.zeros((64, 64))
        x, y = (63*np.randomsimple_segmentation.random((2, 8))).astype(np.int)
        im[x, y] = np.arange(8)

        bigger_points = ndimage.grey_dilation(im, size=(5, 5), structure=np.ones((5, 5)))
        smaller_points = ndimage.grey_erosion(im, size=(5, 5), structure=np.ones((5, 5)))
        plt.figure()
        show_images_and_hists([im,bigger_points,smaller_points])

        square = np.zeros((16, 16))
        square[4:-4, 4:-4] = 1
        dist = ndimage.distance_transform_bf(square)
        dilate_dist = ndimage.grey_dilation(dist, size=(3, 3), \
            structure=np.ones((3, 3)))
        
        erosed_dist = ndimage.grey_erosion(dist, size=(3, 3), \
            structure=np.ones((3, 3)))
            
        plt.figure()
        show_images_and_hists([dist,dilate_dist,erosed_dist])

    def opennning_example():
        """Opening: erosion + dilation:"""
        a = np.zeros((5,5), dtype=np.uint8)
        a[1:4, 1:4] = 1; a[4, 4] = 1
        # Opening removes small objects
        a_no_small = ndimage.binary_opening(a, structure=np.ones((3,3))).astype(np.uint8)
        # Opening can also smooth corners
        a_smooth_corners = ndimage.binary_opening(a).astype(np.uint8)
        
        plt.figure()
        show_images_and_hists([a*255,a_no_small*255,a_smooth_corners*255])

    def edge_detection_example():    
        im = np.zeros((256, 256))        
        im[64:-64, 64:-64] = 1
        im = ndimage.rotate(im, 15, mode='constant')        
        im = ndimage.gaussian_filter(im, 8)
        edge_detection(im,show_result=True)

    def segmentation_example():   
        n = 10
        l = 256
        im = np.zeros((l, l)).astype(np.float64)
        points = l*np.random.random((2, n**2))
        im[(points[0]).astype(np.int), (points[1]).astype(np.int)] = 1
        im = ndimage.gaussian_filter(im, sigma=l/(4.*n))    
        mask = (im > im.mean()).astype(np.float64)
        mask += 0.1 * im
        img = mask + 0.2*np.random.randn(*mask.shape)
        # Segmentation
        b_img = simple_segmentation(input_image=img, show_result=False)
        clear_seg = openning_clossing_clear(b_img, show_result=False)
        plt.figure()
        show_images_and_hists([img, b_img.astype(float), clear_seg.astype(float)],
                       titles=['Input','Segmentation - %.2f' % (np.mean(img)), 'Openning/Clossing'],
                      colorbar=True)
        
        img = read_image('blood1','.PNG','../../datasets/')
        img = median_filter(img,size=5,show_result=True)
        b_img = simple_segmentation(input_image=img, show_result=False)
        clear_seg = openning_clossing_clear(b_img,size=4, show_result=False)
        rec_seg = reconstruct_clear(b_img,size=8,show_result=False)
        plt.figure()
        show_images_and_hists([img, b_img.astype(float), clear_seg.astype(float),rec_seg.astype(float)],
                       titles=['Input','Segmentation - %.2f' % (np.mean(img)), 'Openning/Clossing', 'Reconstruct'],
                      colorbar=True) 
        

        
    #save_image_example()
    #show_image_example()
    #read_image_example()
    #show_hist_example()
    #show_image_and_hist_example()
    #gaussian_filter_example()
    #uniform_filter_example()    
    #sharpenning_filter_example()    
    #insert_noise_example()
    #denoising_example()   
    #denoising_example2()   
    #denoising_example3()
    #erosion_example()
    #dilatation_example()
    #opennning_example()
    #edge_detection_example()
    segmentation_example()    
    plt.show()
    
if __name__ == '__main__':  # if we're running file directly and not importing it
   test()
     
       
  
