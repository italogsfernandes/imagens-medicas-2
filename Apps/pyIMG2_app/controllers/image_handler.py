# -*- coding: utf-8 -*-
import sys
# ------------------------------------------------------------------------------
import numpy as np  # Images are handled as nparray
import matplotlib.pyplot as plt  # Showing images
# ------------------------------------------------------------------------------
sys.path.append('../../toolbox/python')
import scipy_toolbox  # Custom toolbox with image processing functions
# ------------------------------------------------------------------------------


def equalize_image(input_image):
    """input_image show be uint8 ou float64"""
    if input_image.dtype == np.uint8:
        max_value = 255
        min_value = 0
    elif input_image.dtype == np.float64:
        max_value = 0
        min_value = 255

    img_max = input_image.max()
    img_min = input_image.min()

    corrected_image = input_image.astype(np.float64)
    corrected_image = min_value + corrected_image*(max_value-min_value)/(img_max-img_min)
    corrected_image = corrected_image.astype(input_image.dtype)

    return corrected_image


def change_format(input_image, dtype):
    output_image = input_image.astype(dtype)
    return output_image


def change_brightness(input_image, level):
    output_image = input_image.astype(np.float64) + level
    output_image[output_image > 255] = 255
    output_image[output_image < 0] = 0
    output_image = output_image.astype(input_image.dtype)
    return output_image


def change_contrast(input_image, level):
    output_image = input_image * level
    output_image[output_image > 255] = 255
    output_image[output_image < 0] = 0
    output_image = output_image.astype(input_image.dtype)
    return output_image


class ImageModifier:
    def __init__(self,modifier_type='', name='', param={}):
        self.modifier_type = modifier_type
        self.name = name
        self.param = param

    def apply_modifier(self, input_image):
        if self.modifier_type == 'basic':
            return self.apply_basic(input_image)
        elif self.modifier_type == 'noise':
            return self.apply_noise(input_image)
        elif self.modifier_type == 'filter':
            return self.apply_filter(input_image)
        elif self.modifier_type == 'morphology':
            return self.apply_morph(input_image)
        elif self.modifier_type == 'segmentation':
            return self.apply_seg(input_image)
        else:
            raise NotImplementedError

    def apply_basic(self, input_image):
        if self.name == 'format':
            return change_format(input_image,**self.param)
        elif self.name == 'brightness':
            return change_brightness(input_image,**self.param)
        elif self.name == 'contrast':
            return change_contrast(input_image,**self.param)
        elif self.name == 'equalize':
            return equalize_image(input_image)
        else:
            raise NotImplementedError

    def apply_noise(self, input_image):
        output_image = \
            scipy_toolbox.insert_noise(input_image, self.name,
                                       False, **self.param)
        return output_image

    def apply_filter(self, input_image):
        output_image = \
            scipy_toolbox.apply_filter(input_image, self.name,
                                       False, **self.param)
        return output_image

    def apply_morph(self, input_image):
        output_image = \
            scipy_toolbox.apply_math_morphologie(
                input_image,
                self.name,
                self.param['morph_op'],
                self.param['size'],
                False)
        return output_image

    def apply_seg(self, input_image):
        if self.name == 'histogram':
            output_image = input_image > self.param['threshold']
            output_image = output_image.astype(np.float64)
            return output_image

    def __str__(self):
        return "Modifier: %s - %s - %s" % (self.modifier_type, self.name, self.param)

    @staticmethod
    def from_string(str_modifier):
        a = str_modifier.split('Modifier: ')[1]
        m_type = a.split(' - ')[0]
        m_name = a.split(' - ')[1]
        m_dict = a.split(' - ')[2]
        m_dict = m_dict[1:-1]
        m_dict_pars = m_dict.split(', ')
        m_keys = [b.split(': ')[0] for b in m_dict_pars]
        m_values = [b.split(': ')[1] for b in m_dict_pars]
        return ImageModifier(m_type,m_name,m_dict)


def test():
    pass

if __name__ == "__main__":
    test()
