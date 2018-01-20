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
        max_value = 1.0
        min_value = -1.0

    img_max = input_image.max()
    img_min = input_image.min()

    corrected_image = input_image.astype(np.float64)
    corrected_image = min_value + corrected_image*(max_value-min_value)/(img_max-img_min)
    corrected_image = corrected_image.astype(input_image.dtype)

    return corrected_image


class ImageModifier:
    def __init__(self, name, param):
        self.modifier_type = None
        self.name = name
        self.param = param

    def apply_modifier(self, input_image):
        output_image = np.copy(input_image)
        return output_image

    def __str__(self):
        return "Modifier: %s - %s - %s" % (self.modifier_type, self.name, self.param)


class NoiseModifier(ImageModifier):
    def __init__(self, name, param):
        ImageModifier.__init__(self, name, param)
        self.modifier_type = 'noise'

    def apply_modifier(self, input_image):
        output_image = \
            scipy_toolbox.insert_noise(input_image, self.name,
                                       False, **self.param)
        return output_image


class FilterModifier(ImageModifier):
    def __init__(self, name, param):
        ImageModifier.__init__(self, name, param)
        self.modifier_type = 'filter'

    def apply_modifier(self, input_image):
        output_image = \
            scipy_toolbox.apply_filter(input_image, self.name,
                                       False, **self.param)
        return output_image


class MathMorphModifier(ImageModifier):
    def __init__(self, name, morph_op, size):
        ImageModifier.__init__(self, name, {'morph_op': morph_op, 'size': size})
        self.modifier_type = 'morph'

    def apply_modifier(self, input_image):
        output_image = \
            scipy_toolbox.apply_math_morphologie(
                input_image,
                self.name,
                self.param['morph_op'],
                self.param['size'],
                False)
        return output_image


def test():
    my_img = np.ones((100, 100), dtype=np.uint8) * 127
    my_mod = NoiseModifier('uniform', {'low': 0.0, 'high': 80.0, 'amount': 1.0})
    out_img = my_mod.apply_modifier(my_img)
    plt.figure()
    scipy_toolbox.show_images_and_hists([my_img, out_img], ['gray', 'noise'])

    my_filt = FilterModifier('median', {'size': 3})
    filt_img = my_filt.apply_modifier(out_img)
    plt.figure()
    scipy_toolbox.show_images_and_hists([out_img, filt_img], ['noise', 'median'])

    my_morph = MathMorphModifier('erosion', 'grey', 3)
    morph_img = my_morph.apply_modifier(out_img)
    plt.figure()
    scipy_toolbox.show_images_and_hists([out_img, morph_img], ['noise', 'morph'])

    plt.show()

if __name__ == "__main__":
    test()
