# -*- coding: utf-8 -*-
"""Ferramentas para manipulação de imagens utilizando a biblioteca scipy

Neste modulo estão implementadas diversas funções úteis para o processamento de
imagens medicas. Estas foram baseadas nos exemplos presentes no seguinte link:
http://www.scipy-lectures.org/advanced/image_processing/index.html

Sendo eles:
    2.6.1. Opening and writing to image files
    2.6.2. Displaying images
    2.6.3. Basic manipulations
    2.6.4. Image filtering
    2.6.5. Feature extraction
    2.6.6. Measuring objects properties: ndimage.measurements

Outro link importante:
https://docs.scipy.org/doc/scipy/reference/tutorial/ndimage.html

Estão também as funções separadas por categorias:
    - Displaysing images
    - Inserting noises
    - Applying filters
    - Applying mathematical morphologies
    - Applying segmentation methods

License
-------
*THE BEERWARE LICENSE* (Revision 42):
Italo Fernandes wrote this code. As long as you retain this 
notice, you can do whatever you want with this stuff. If we
meet someday, and you think this stuff is worth it, you can
buy me a beer in return.

Author
------
Italo Gustavo Sampaio Fernandes
    Contact: italogsfernandes@gmail.com
    Git: www.github.com/italogfernandes
    
Janeiro de 2018

Organization
------------
FEDERAL UNIVERSITY OF UBERLANDIA
Faculty of Electrical Engineering
Biomedical Engineering Lab

Examples
-------
Os exemplos de uso foram immplementados na função test, está é chamada se
o arquivo for executado diretamente e não importado::

    $ python scipy_toolbox.py


É preciso selecionar qual exemplo você deseja visualizar a execução. Leia o
código da função test() para mais informações.

"""
from scipy import misc # Opening and clossing
import matplotlib.pyplot as plt # Showing the images
import numpy as np # Image manipulation as nparray
from scipy import ndimage # Gaussian filter

# ------------------------------------------------------------------------------
## Atributes
# ------------------------------------------------------------------------------
noise_names = ('uniform',
               'gaussian',
               'rayleight',
               'exponential',
               'gamma',
               'salt_and_pepper')
"""str tuple: tuple with the possible noises that you can add to a image"""

noise_params = {'uniform':{'low':0.0,'high':80.0,'amount':1.0},
                'gaussian':{'mean':5.0,'str':30.0,'amount':1.0},
                'rayleight':{'scale':20.0,'amount':1.0},
                'exponential':{'scale':5.0,'amount':1.0},
                'gamma':{'shape':1.0,'scale':8.0,'amount':1.0},
                'salt_and_pepper':{'s_vs_p':0.5,'amount':0.004}}
"""dict: for each possible noise, here there are the params and default values"""
# ------------------------------------------------------------------------------
filter_names = ('gaussian',
                'uniform',
                'median',
                'maximum',
                'minimum',
                'sharpening',
                'percentile',
                'wiener',
                'sobel')
"""str tuple: tuple of all implemented filters, that can be used with filter_image"""

filter_params = {'gaussian': {'sigma': 3},
                 'uniform': {'size': 3},
                 'median': {'size': 3},
                 'maximum': {'size': 3},
                 'minimum': {'size': 3},
                 'sharpening': {'alpha': 30, 'filter_sigma': 1},
                 'percentile': {'percentile':75,'size': 3},
                 'wiener':{},
                 'sobel':{}}
"""dict: for each possible filter, here there are the params and default values"""
# ------------------------------------------------------------------------------
mathematical_morphologies_names = ('erosion',
                                   'dilation',
                                   'opening',
                                   'closing',
                                   'propagation',
                                   'reconstruction',
                                   'open/close',
                                   'full_reconstruction')
"""str tuple: tuple of all implemented  mathematical morphologie that you can apply"""

mathematical_morphologies_options = ('binary','grey')
"""str tuple: tuple of option for each mathematical morphologie"""
# ------------------------------------------------------------------------------
segmentation_names = ('histogram',
                      'spectral_clustering')
"""str tuple: tuple of all implemented  segmentation methods"""

segmentation_params = {'histogram':{'mode':'mean'},
                       'spectral_clustering':{'qnt_clusters':4}}
"""dict: for each possible segmentation, here there are the params and default values"""
# ------------------------------------------------------------------------------
## Functions
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
## Displaying images (2.6.2)
# ------------------------------------------------------------------------------
def show_image(input_image,title=None, colorbar=False):
    if input_image.dtype == np.float64:
        min_value = min(input_image.ravel())
        max_value = max(input_image.ravel())
    else:
        min_value = np.iinfo(input_image.dtype).min
        max_value = np.iinfo(input_image.dtype).max    
    im = plt.imshow(input_image, cmap=plt.cm.grey,clim=(min_value, max_value))
    if colorbar:
        plt.colorbar(orientation='vertical')
    if not title is None:
        plt.title(title)
    return im

def show_hist(input_image,title=None):
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
## Inserting Noise
# ------------------------------------------------------------------------------
def insert_uniform_noise(input_image, low=0, high=80, amount=1.0):
    return (input_image + amount * np.random.uniform(low,high,input_image.shape))
    
def insert_gaussian_noise(input_image, mean=5, std=30, amount=1.0):
    return (input_image + amount * np.random.normal(mean,std,input_image.shape))

def insert_rayleight_noise(input_image, scale=20, amount=1.0):
    return (input_image + amount * np.random.rayleigh(scale,input_image.shape))
      
def insert_exponential_noise(input_image, scale=5, amount=1.0):
    return (input_image + amount * np.random.exponential(scale,input_image.shape))

def insert_gamma_noise(input_image, shape=1, scale=8, amount=1.0):
    return (input_image + amount * np.random.gamma(shape,scale,input_image.shape))

def insert_salt_and_pepper_noise(input_image,s_vs_p=0.5,amount=0.004):
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
    return (output_image)

def insert_noise(input_image, noise_type, show_result=False, *args, **kwargs):
    """
    Insert a selected noise to a image.
    
    Parameters
    ----------
    input_image : nparray
        Represents the image that you want to add noise.
    filter_type: str
        Must in one of:
                'uniform',
                'gaussian',
                'rayleight',
                'exponential',
                'gamma',
                'salt_and_pepper'
    show_result: Boolean
            If True, the result is plotted using matplotlib, default is False.
    *args: Arguments of the selected noise, see details for more information.
    **kwargs: The key arguments of the selected noise, see details for more information.
    
    Returns
    -------
    nparray
        The image with the noise as the same format of the input.
        
    Details
    -------
    Arguments for the noise and the default values:
    =================  =====================================
    Filter             Kwargs       
    =================  =====================================
    'uniform'          'low':0.0,'high':80.0,'amount':1.0
    'gaussian'         'mean':5.0,'str':30.0,'amount':1.0
    'rayleight'        'scale':20.0,'amount':1.0
    'exponential'      'scale':5.0,'amount':1.0
    'gamma'            'shape':1.0,'scale':8.0,'amount':1.0
    'salt_and_pepper'  's_vs_p':0.5,'amount':0.004
    =================  =====================================
    This details also are defined in this module as a argument.      
    """
    if noise_type not in noise_names:
        raise(NotImplemented)                      
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
                                              
    output_image = output_image.astype(input_image.dtype) # input format
    return output_image
  
# ------------------------------------------------------------------------------
## Image filtering
# ------------------------------------------------------------------------------
def sharpenning_filter(input_image, alpha = 30, filter_sigma=1,show_result=False):
    filter_blurred_f = ndimage.gaussian_filter(input_image, filter_sigma)
    sharpened = input_image + alpha * (input_image - filter_blurred_f)
    if show_result:
        show_images_and_hists([input_image,sharpened],['Input', 'Sharpened'])
    return sharpened

def sobel_filter(input_image):
    sx = ndimage.sobel(input_image, axis=0, mode='constant')
    sy = ndimage.sobel(input_image, axis=1, mode='constant')
    sob = np.hypot(sx, sy)
    return sob
    
def apply_filter(input_image, filter_type, show_result=False, *args, **kwargs):
    """
    Apply a selected filter to a image.
    
    Parameters
    ----------
    input_image : nparray
        Represents the image to be filtered
    filter_type: str
        Must in one of:
                'gaussian',
                'uniform',
                'median',
                'maximum',
                'minimum',
                'sharpening',
                'percentile',
                'wiener',
                'sobel'
    show_result: Boolean
            If True, the result is plotted using matplotlib, default is False.
    *args: Arguments of the selected filter, see details for more information.
    **kwargs: The key arguments of the selected filter, see details for more information.
    
    Returns
    -------
    nparray
        The filtered image as the same format of the input.
        
    Details
    -------
    Arguments for the filters and the default values:
    =============  ===========================
    Filter         Kwargs       
    =============  ===========================
    'gaussian'     sigma: 3   
    'uniform'      size: 3
    'median'       size: 3
    'maximum'      size: 3
    'minimum'      size: 3
    'sharpening'   alpha: 30, filter_sigma: 1
    'percentile'   percentile: 75, size: 3
    'wiener'       NotImplement
    'sobel'        None
    =============  ===========================
    This details also are defined in this module as a argument.
    """
    if filter_type not in filter_names:
        raise(NotImplemented)                      
    if filter_type == 'gaussian':
        output_image = ndimage.gaussian_filter(input_image, *args, **kwargs)
    elif filter_type == 'uniform':
        output_image = ndimage.uniform_filter(input_image, *args, **kwargs)
    elif filter_type == 'median':
        output_image = ndimage.median_filter(input_image, *args, **kwargs)
    elif filter_type == 'maximum':
        output_image = ndimage.maximum_filter(input_image, *args, **kwargs)
    elif filter_type == 'minimum':
        output_image = ndimage.minimum_filter(input_image, *args, **kwargs) 
    elif filter_type == 'sharpening':
        output_image = sharpenning_filter(input_image, *args, **kwargs) 
    elif filter_type == 'percentile':
        output_image = ndimage.percentile_filter(input_image, *args, **kwargs)        
    elif filter_type == 'wiener': # TODO: finish the wiener filter
        raise(NotImplemented)        
    elif filter_type == 'sobel':
        output_image = sobel_filter(input_image)       

    if show_result:
        show_images_and_hists([input_image,output_image],
                              titles=['Input', 'Output Image - %s%s\n%s - %s' %
                              ("Filter: ", filter_type, str(args),str(kwargs))],
                              colorbar=True)
    
    output_image = output_image.astype(input_image.dtype) # input format
    return output_image
    
# -----------file-------------------------------------------------------------------
## Mathematical Morphologie
# ------------------------------------------------------------------------------
      
def apply_math_morphologie(input_image, morph_type ,morph_op='binary', size=3,
                           show_result=False):
    """
    Apply a mathematical morphologie to a image.
    
    Parameters
    ----------
    input_image : nparray
        Represents the image that you want to apply the morphologie
    morph_type: str
        Must be one of:
                'erosion',
                'dilation',
                'opening',
                'closing',
                'propagation',
                'reconstruction',
                'open/close',
                'full_reconstruction'
    morph_op: str
        'binary' or 'grey', representing the two types of supported image
    size: int
        The morphologie structure is a matrix of ones with sizeXsize
    show_result: Boolean
            If True, the result is plotted using matplotlib, default is False.
    
    Returns
    -------
    nparray
        The image after morphologia, as the same format of the input.
    
    Note
    ----
    Some configurations may not exit.
    They are:
        grey propagation
        grey reconstruction
        grey full_reconstruction
    """
    if not morph_type in mathematical_morphologies_names:
        raise(NotImplemented)
    if not morph_op in mathematical_morphologies_options:
        raise(NotImplemented)
    
    if morph_op == 'binary':
        if morph_type == 'erosion':
            output_image = ndimage.binary_erosion(input_image,structure=np.ones((size,size)))
        elif morph_type == 'dilation':
            output_image = ndimage.binary_dilation(input_image,structure=np.ones((size,size)))
        elif morph_type == 'opening':
            output_image = ndimage.binary_opening(input_image,structure=np.ones((size,size)))
        elif morph_type == 'closing':
            output_image = ndimage.binary_closing(input_image,structure=np.ones((size,size)))
        elif morph_type == 'propagation':
            output_image = ndimage.binary_propagation(input_image,structure=np.ones((size,size)))            
        elif morph_type == 'reconstruction':
            eroded_img = ndimage.binary_erosion(input_image,structure=np.ones((size,size)))        
            output_image = ndimage.binary_propagation(eroded_img, structure=np.ones((size,size)), mask=input_image)
        elif morph_type == 'open/close':
            open_img = ndimage.binary_opening(input_image,structure=np.ones((size,size))) # Remove small white regions
            output_image = ndimage.binary_closing(open_img,structure=np.ones((size,size))) # Remove small black hole
        elif morph_type == 'full_reconstruction':
            eroded_img = ndimage.binary_erosion(input_image,structure=np.ones((size,size)))        
            reconstruct_img = ndimage.binary_propagation(eroded_img, structure=np.ones((size,size)), mask=input_image)
            tmp = np.logical_not(reconstruct_img)
            eroded_tmp = ndimage.binary_erosion(tmp,structure=np.ones((size,size)))
            output_image = np.logical_not(ndimage.binary_propagation(eroded_tmp,structure=np.ones((size,size)), mask=tmp))
    elif morph_op == 'grey':
        if morph_type == 'erosion':
            output_image = ndimage.grey_erosion(input_image,size=size)        
        elif morph_type == 'dilation':
            output_image = ndimage.grey_dilation(input_image,size=size) 
        elif morph_type == 'opening':
            output_image = ndimage.grey_opening(input_image,size=size)
        elif morph_type == 'closing':
            output_image = ndimage.grey_closing(input_image,size=size)
        elif morph_type == 'propagation':
            raise(NotImplemented)            
        elif morph_type == 'reconstruction':
            raise(NotImplemented)
        elif morph_type == 'open/close':
            open_img = ndimage.grey_opening(input_image,size=size) # Remove small white regions
            output_image = ndimage.grey_closing(open_img,size=size) # Remove small black hole
        elif morph_type == 'full_reconstruction':
            raise(NotImplemented)
        
    if show_result:
        show_images_and_hists([input_image,output_image],
                              titles=['Input', 'Output Image - %s%s\n%s - %s' %
                              ("Morph: ", morph_type, str(morph_op),str(size))],
                              colorbar=True)
    
    output_image = output_image.astype(input_image.dtype) # input format
    return output_image

# ------------------------------------------------------------------------------
# Segmentation
# ------------------------------------------------------------------------------
def apply_hist_segmentation(input_image, mode='mean', show_result=False):
    """Histogram-based segmentation (no spatial information)"""
    if mode == 'mean':    
        th = np.mean(input_image)
    elif mode == 'median':
        th = np.median(input_image)
    else:
        raise(NotImplemented)
    binary_img = input_image > th
    if show_result:
        show_images_and_hists([input_image, binary_img.astype(float)],
                               titles=['Input','Segmentation - %.2f' % (th)],
                              colorbar=True)
    return binary_img

# ------------------------------------------------------------------------------
## Functions based in scipy example
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
## Opening and writing to image files (2.6.1.)
# ------------------------------------------------------------------------------
def save_image(input_image,name=None,extension='.png',folder=None):
    """
    Save a image in a determined format and folder
    """    
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
## Image filtering (2.6.4.)
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
    
# ------------------------------------------------------------------------------
# Feature Extraction - Edge detection (2.6.5.1.)
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
# Segmentation (2.6.6.)
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
        my_image = read_image('blood1','.PNG','../../datasets/')
        show_image(my_image)
    
    def show_hist_example():
        my_image = read_image('blood1','.PNG','../../datasets/')
        show_hist(my_image)
        
    def show_image_and_hist_example():
        my_image = read_image('blood1','.PNG','../../datasets/')
        show_image_and_hist(my_image,'Blood', 'Histogram of Blood')
    
    def gaussian_filter_example():
        my_image = read_image('blood1','.PNG','../../datasets/')
        gaussian_filter(my_image,show_result=True)
    
    def uniform_filter_example():
        my_image = read_image('blood1','.PNG','../../datasets/')        
        uniform_filter(my_image,size=11,show_result=True)
        
    def sharpenning_filter_example():        
        face = misc.face(grey=True).astype(np.float64)
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
        f = misc.face(grey=True)#.astype(np.float64)
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
        # Also work for grey values
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
        # TODO: See also Other Scientific Packages provide algorithms that can
        #             be useful for image processing. In this example, we use 
        #             the spectral clustering function of the scikit-learn in 
        #             order to segment glued objects.
        

        
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
     
       
  
