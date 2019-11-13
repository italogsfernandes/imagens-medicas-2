from PIL import Image

from django.db import models

from django.template.defaultfilters import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model
from django.db.models import CharField, Value

import numpy as np  # Image manipulation as nparray
from scipy import misc  # Open images
from scipy import ndimage  # Filters
from scipy import signal  # Filters
import imageio

User = get_user_model()


class ImageModel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True, verbose_name=_("Slug"), null=True, blank=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    comments = models.TextField(blank=True, default='')

    original_image = models.ImageField()
    original_image_thumbnail = ImageSpecField(
        source='original_image',
        processors=[ResizeToFit(width=100, height=100, upscale=False)],
        format='JPEG',
        options={'optimize': True}
    )

    edited_image = models.ImageField()
    edited_image_thumbnail = ImageSpecField(
        source='original_image',
        processors=[ResizeToFit(width=100, height=100, upscale=False)],
        format='JPEG',
        options={'optimize': True}
    )

    @property
    def get_image_informations(self):
        '''
        Example:
            >>> img.width
            190
            >>> img.height
            185
            >>> img.text
            {'Description':
                '\n\nOriginal filename: Blood cells'
                '\n\nCopyright J. C. Russ, The Image Processing Handbook'
                '\nSecond Edition, 1994, CRC Press, Boca Raton,
                '\nISBN 0-8493-2516-1. Used with permission.\n'}
            >>> img.size
            (190, 185)
            >>> img.mode
            'L'
            >>> img.info
            {'Description':
                '\n\nOriginal filename: Blood cells'
                '\n\nCopyright J. C. Russ, The Image Processing Handbook'
                '\nSecond Edition, 1994, CRC Press, Boca Raton,
                '\nISBN 0-8493-2516-1. Used with permission.\n',
             'gamma': 0.45455
            }
            >>> img.getextrema()
            (46, 255)
            >>> img.getbbox()
            (0, 0, 190, 185)
            >>> img.get_format_mimetype()
            'image/png'
            >>> img.format_description
            'Portable network graphics'
            >>> img.format
            'PNG'
            >>> img.entropy()
            6.361345355074605
        '''
        img = Image.open(self.original_image.path)
        image_info_dict = {
            "width": img.width,
            "height": img.height,
            "size": img.size,
            "mode": img.mode,
            "info": img.info,
            "getextrema": img.getextrema(),
            "getbbox": img.getbbox(),
            "get_format_mimetype": img.get_format_mimetype(),
            "format_description": img.format_description,
            "format": img.format,
            "entropy": img.entropy(),
        }
        img.close()
        return image_info_dict

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(ImageModel, self).clean()

    def reset_edited_image(self):
        complete_file_name = self.original_image.path
        file_name = complete_file_name.split('/')[-1]
        file_path = complete_file_name.split('/')[:-1]
        new_file_name = 'EDITED-' + file_name
        file_path.append(new_file_name)
        edited_image_file_path = '/'.join(file_path)
        # Open the image file
        original_image = imageio.imread(complete_file_name)
        # Save the result
        imageio.imwrite(edited_image_file_path, original_image)
        self.edited_image = new_file_name
        self.save()

    def apply_all_modifiers(self):
        modifiers_query = self.get_modifiers_list().order_by('created_date')
        for modifier in modifiers_query:
            if modifier['modifier'] == 'intensity':
                modifier_obj = self.intensityimagemodifier_set.get(
                    pk=modifier['pk']
                )
            elif modifier['modifier'] == 'noise':
                modifier_obj = self.noiseimagemodifier_set.get(
                    pk=modifier['pk']
                )
            elif modifier['modifier'] == 'filter':
                modifier_obj = self.filterimagemodifier_set.get(
                    pk=modifier['pk']
                )
            modifier_obj.apply_modifier()

    def get_modifiers_list(self):
        intensities = self.intensityimagemodifier_set.all().values(
            'pk',
            'saved_name',
            'created_date',
        )
        noises = self.noiseimagemodifier_set.all().values(
            'pk',
            'saved_name',
            'created_date',
        )
        filters = self.filterimagemodifier_set.all().values(
            'pk',
            'saved_name',
            'created_date',
        )
        intensities = intensities.annotate(modifier=Value(
            'intensity', output_field=CharField()))
        noises = noises.annotate(modifier=Value(
            'noise', output_field=CharField()))
        filters = filters.annotate(modifier=Value(
            'filter', output_field=CharField()))
        all_modifiers = intensities.union(noises)
        all_modifiers = all_modifiers.union(filters)
        all_modifiers = all_modifiers.order_by('-created_date')
        return all_modifiers

    # TODO: add delete storage. self.image.storage.delete
    def __str__(self):
        return self.name


class IntensityImageModifier(models.Model):
    BRIGHTNESS = 'BRIGHTNESS'
    CONTRAST = 'CONTRAST'
    NEGATIVE = 'NEGATIVE'
    IDENTITY = 'IDENTITY'
    LOGARITHMIC = 'LOGARITHMIC'
    EXPONENTIAL = 'EXPONENTIAL'
    POWER = 'POWER'

    SIMPLE_MODIFER_CHOICES = (
        (BRIGHTNESS, _('Brightness')),
        (CONTRAST, _('Contrast')),
        (NEGATIVE, _('Negative')),
        (IDENTITY, _('Identity')),
        (LOGARITHMIC, _('Logarithmic')),
        (EXPONENTIAL, _('Exponential')),
        (POWER, _('Power')),
    )

    # As they are saved in the db is not a good thing to save the translation
    # but it's used only to present to the user a name before the arg_value
    # and there should not be queries depending on the argument name
    ARGUMENT_NAMES = {
        BRIGHTNESS: _("shades"),
        CONTRAST: _("factor"),
        NEGATIVE: _("percentage"),
        IDENTITY: _("identity"),
        LOGARITHMIC: _("c"),
        EXPONENTIAL: _("gamma"),
        POWER: _("factor"),
    }

    type_of_modifier = models.CharField(
        verbose_name=_('Type of Modifier *'),
        max_length=max([len(e[0]) for e in SIMPLE_MODIFER_CHOICES]),
        choices=SIMPLE_MODIFER_CHOICES,
    )

    argument_name = models.CharField(max_length=255)
    argument_value = models.DecimalField(
        decimal_places=2, max_digits=12, default=0
    )

    imagem = models.ForeignKey(
        ImageModel,
        on_delete=models.CASCADE,
    )

    created_date = models.DateTimeField(auto_now_add=True)
    applied_date = models.DateTimeField(auto_now=True)

    saved_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return _("Intensity {} ({}: {})").format(
            self.get_type_of_modifier_display(),
            self.argument_name,
            self.argument_value,
        )

    def apply_brightness(self, input_image, shades):
        output_image = input_image.astype(np.float64) + float(shades)
        output_image[output_image > 255] = 255
        output_image[output_image < 0] = 0
        output_image = output_image.astype(input_image.dtype)
        return output_image

    def apply_contrast(self, input_image, factor):
        output_image = input_image.astype(np.float64) * float(factor)
        output_image[output_image > 255] = 255
        output_image[output_image < 0] = 0
        output_image = output_image.astype(input_image.dtype)
        return output_image

    def apply_negative(self, input_image, percentage):
        output_image = 255 - input_image.astype(np.float64)
        output_image[output_image > 255] = 255
        output_image[output_image < 0] = 0
        output_image = (
            input_image.astype(np.float64) * (1.0 - percentage) +
            output_image * percentage
        )
        output_image[output_image > 255] = 255
        output_image[output_image < 0] = 0
        output_image = output_image.astype(input_image.dtype)
        return output_image

    def apply_identity(self, input_image):
        return input_image.copy()

    def apply_logarithmic(self, input_image, c):
        output_image = float(c) * np.log10(1 + input_image.astype(np.float64))
        output_image[output_image > 255] = 255
        output_image[output_image < 0] = 0
        output_image = output_image.astype(input_image.dtype)
        return output_image

    def apply_exponential(self, input_image, gamma):
        output_image = np.power(input_image.astype(np.float64), float(gamma))
        output_image[output_image > 255] = 255
        output_image[output_image < 0] = 0
        output_image = output_image.astype(input_image.dtype)
        return output_image

    def apply_power(self, input_image, factor):
        return input_image

    def apply_modifier(self):
        complete_file_name = self.imagem.edited_image.path
        # Open the image file
        input_image = imageio.imread(complete_file_name)
        # Save the result
        if self.type_of_modifier == self.BRIGHTNESS:
            output_image = self.apply_brightness(
                input_image, float(self.argument_value)
            )
        elif self.type_of_modifier == self.CONTRAST:
            output_image = self.apply_contrast(
                input_image, float(self.argument_value)
            )
        elif self.type_of_modifier == self.NEGATIVE:
            output_image = self.apply_negative(
                input_image, float(self.argument_value)
            )
        elif self.type_of_modifier == self.IDENTITY:
            output_image = self.apply_identity(
                input_image
            )
        elif self.type_of_modifier == self.LOGARITHMIC:
            output_image = self.apply_logarithmic(
                input_image, float(self.argument_value)
            )
        elif self.type_of_modifier == self.EXPONENTIAL:
            output_image = self.apply_exponential(
                input_image, float(self.argument_value)
            )
        elif self.type_of_modifier == self.POWER:
            output_image = self.apply_power(
                input_image, float(self.argument_value)
            )
        else:
            raise NotImplementedError()

        imageio.imwrite(complete_file_name, output_image)
        return output_image


class NoiseImageModifier(models.Model):
    UNIFORM = 'uniform'
    GAUSSIAN = 'gaussian'
    RAYLEIGHT = 'rayleight'
    EXPONENTIAL = 'exponential'
    GAMMA = 'gamma'
    SALT_AND_PEPPER = 'salt_and_pepper'

    NOISE_MODIFIER_CHOICES = (
        (UNIFORM, _('Uniform')),
        (GAUSSIAN, _('Gaussian')),
        (RAYLEIGHT, _('Rayleight')),
        (EXPONENTIAL, _('Exponential')),
        (GAMMA, _('Gamma')),
        (SALT_AND_PEPPER, _('Salt and Pepper')),
    )

    ARGUMENT1_NAMES = {
        UNIFORM: "low",
        GAUSSIAN: "mean",
        RAYLEIGHT: "scale",
        EXPONENTIAL: "scale",
        GAMMA: "shape",
        SALT_AND_PEPPER: "s_vs_p",
    }
    ARGUMENT2_NAMES = {
        UNIFORM: "high",
        GAUSSIAN: "std",
        RAYLEIGHT: "rayleight",
        EXPONENTIAL: "exponential",
        GAMMA: "scale",
        SALT_AND_PEPPER: "salt_and_pepper",
    }

    noise_type = models.CharField(
        verbose_name=_('Noise Type: '),
        max_length=max([len(e[0]) for e in NOISE_MODIFIER_CHOICES]),
        choices=NOISE_MODIFIER_CHOICES,
        blank=False,
        null=False,
    )

    argument1_name = models.CharField(max_length=255, blank=False, null=False)
    argument1_value = models.DecimalField(
        decimal_places=2, max_digits=12, default=0,
        blank=False, null=False,
    )

    argument2_name = models.CharField(max_length=255, blank=True, null=True)
    argument2_value = models.DecimalField(
        decimal_places=2, max_digits=12, default=0,
        blank=True, null=True,
    )

    # TODO: min 0 to max 1
    amount_value = models.DecimalField(
        verbose_name=_('Amount: '),
        decimal_places=2, max_digits=12, default=0,
        blank=False, null=False,
    )

    imagem = models.ForeignKey(
        ImageModel,
        on_delete=models.CASCADE,
    )

    created_date = models.DateTimeField(auto_now_add=True)
    applied_date = models.DateTimeField(auto_now=True)

    saved_name = models.CharField(max_length=255, blank=True, null=True)

    def insert_uniform_noise(self, input_image, low=0, high=80, amount=1.0):
        return (
            input_image +
            amount * np.random.uniform(
                low, high,
                input_image.shape
            )
        )

    def insert_gaussian_noise(self, input_image, mean=5, std=30, amount=1.0):
        return (
            input_image +
            amount * np.random.normal(
                mean, std,
                input_image.shape
            )
        )

    def insert_rayleight_noise(self, input_image, scale=20, amount=1.0):
        return (
            input_image +
            amount * np.random.rayleigh(
                scale,
                input_image.shape
            )
        )

    def insert_exponential_noise(self, input_image, scale=5, amount=1.0):
        return (
            input_image +
            amount * np.random.exponential(
                scale,
                input_image.shape
            )
        )

    def insert_gamma_noise(self, input_image, shape=1, scale=8, amount=1.0):
        return (
            input_image +
            amount * np.random.gamma(
                shape, scale,
                input_image.shape
            )
        )

    def insert_salt_and_pepper_noise(self,
                                     input_image, s_vs_p=0.5, amount=0.004):
        min_value = 0
        max_value = 255

        output_image = np.copy(input_image)

        # Salt mode
        num_salt = np.ceil(amount * input_image.size * s_vs_p)
        coords = [
            np.random.randint(
                0, i - 1, int(num_salt)
            ) for i in input_image.shape
        ]
        output_image[coords] = max_value

        # Pepper mode
        num_pepper = np.ceil(amount * input_image.size * (1. - s_vs_p))
        coords = [
            np.random.randint(
                0, i - 1, int(num_pepper)
            ) for i in input_image.shape
        ]
        output_image[coords] = min_value

        return (output_image)

    def apply_modifier(self):
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
                If True, the result is plotted using matplotlib,
                 default is False.
        *args: Arguments of the selected noise,
                see details for more information.
        **kwargs: The key arguments of the selected noise
                    see details for more information.

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
        complete_file_name = self.imagem.edited_image.path
        # Open the image file
        input_image = imageio.imread(complete_file_name)
        # Save the result
        if self.noise_type == self.UNIFORM:
            output_image = self.insert_uniform_noise(
                input_image,
                float(self.argument1_value),
                float(self.argument2_value),
                float(self.amount_value),
            )
        elif self.noise_type == self.GAUSSIAN:
            output_image = self.insert_gaussian_noise(
                input_image,
                float(self.argument1_value),
                float(self.argument2_value),
                float(self.amount_value),
            )
        elif self.noise_type == self.RAYLEIGHT:
            output_image = self.insert_rayleight_noise(
                input_image,
                float(self.argument1_value),
                float(self.amount_value),
            )
        elif self.noise_type == self.EXPONENTIAL:
            output_image = self.insert_exponential_noise(
                input_image,
                float(self.argument1_value),
                float(self.amount_value),
            )
        elif self.noise_type == self.GAMMA:
            output_image = self.insert_gamma_noise(
                input_image,
                float(self.argument1_value),
                float(self.argument2_value),
                float(self.amount_value),
            )
        elif self.noise_type == self.SALT_AND_PEPPER:
            output_image = self.insert_salt_and_pepper_noise(
                input_image,
                float(self.argument1_value),
                float(self.amount_value),
            )
        else:
            raise NotImplementedError()

        output_image = output_image.astype(input_image.dtype)
        imageio.imwrite(complete_file_name, output_image)
        return output_image

    def __str__(self):
        return _("Noise {} ({}: {}, {}: {}, Amount: {})").format(
            self.get_noise_type_display(),
            self.argument1_name,
            self.argument1_value,
            self.argument2_name,
            self.argument2_value,
            self.amount_value,
        )


class FilterImageModifier(models.Model):
    GAUSSIAN = 'gaussian'
    UNIFORM = 'uniform'
    MEDIAN = 'median'
    MAXIMUM = 'maximum'
    MINIMUM = 'minimum'
    SHARPENING = 'sharpening'
    PERCENTILE = 'percentile'
    WIENER = 'wiener'
    SOBEL = 'sobel'
    FILTER_MODIFIER_CHOICES = (
        (GAUSSIAN, _('Gaussian')),
        (UNIFORM, _('Uniform')),
        (MEDIAN, _('Median')),
        (MAXIMUM, _('Maximum')),
        (MINIMUM, _('Minimum')),
        (SHARPENING, _('Sharpening')),
        (PERCENTILE, _('Percentile')),
        (WIENER, _('Wiener')),
        (SOBEL, _('Sobel')),
    )

    ARGUMENT1_NAMES = {
        GAUSSIAN: "sigma",
        UNIFORM: "uniform",
        MEDIAN: "median",
        MAXIMUM: "maximum",
        MINIMUM: "minimum",
        MINIMUM: "minimum",
        SHARPENING: "alpha",
        PERCENTILE: "percentile",
        WIENER: "noise_power",
        SOBEL: "sobel",
    }
    filter_type = models.CharField(
        verbose_name=_('Noise Type: '),
        max_length=max([len(e[0]) for e in FILTER_MODIFIER_CHOICES]),
        choices=FILTER_MODIFIER_CHOICES,
        blank=False,
        null=False,
    )

    # TODO terminar esses filtros
    argument1_name = models.CharField(max_length=255, blank=False, null=False)
    argument1_value = models.DecimalField(
        decimal_places=2, max_digits=12, default=0,
        blank=False, null=False,
    )

    size_value = models.DecimalField(
        verbose_name=_('Amount: '),
        decimal_places=2, max_digits=12, default=0,
        blank=False, null=False,
    )

    imagem = models.ForeignKey(
        ImageModel,
        on_delete=models.CASCADE,
    )

    created_date = models.DateTimeField(auto_now_add=True)
    applied_date = models.DateTimeField(auto_now=True)

    saved_name = models.CharField(max_length=255, blank=True, null=True)

    def sharpenning_filter(self, input_image,
                           alpha=30, filter_sigma=1):
        filter_blurred_f = ndimage.gaussian_filter(input_image, filter_sigma)
        sharpened = input_image + alpha * (input_image - filter_blurred_f)
        return sharpened

    def sobel_filter(self, input_image):
        sx = ndimage.sobel(input_image, axis=0, mode='constant')
        sy = ndimage.sobel(input_image, axis=1, mode='constant')
        sob = np.hypot(sx, sy)
        return sob

    def apply_modifier(self, input_image):
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
        *args: Arguments of the selected filter,
            see details for more information.
        **kwargs: The key arguments of the selected filter,
            see details for more information.

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
        'wiener'       noise power and size
        'sobel'        None
        =============  ===========================
        This details also are defined in this module as a argument.
        """
        complete_file_name = self.image.edited_image.path
        # Open the image file
        input_image = imageio.imread(complete_file_name)
        # Apply the Modifier
        if self.filter_type == self.GAUSSIAN:
            output_image = ndimage.gaussian_filter(
                input_image,
                sigma=float(self.argument1_value),
            )
        elif self.filter_type == self.UNIFORM:
            output_image = ndimage.uniform_filter(
                input_image,
                size=int(self.size_value),
            )
        elif self.filter_type == self.MEDIAN:
            output_image = ndimage.median_filter(
                input_image,
                size=int(self.size_value),
            )
        elif self.filter_type == self.MAXIMUM:
            output_image = ndimage.maximum_filter(
                input_image,
                size=int(self.size_value),
            )
        elif self.filter_type == self.MINIMUM:
            output_image = ndimage.minimum_filter(
                input_image,
                size=int(self.size_value),
            )
        elif self.filter_type == self.SHARPENING:
            output_image = self.sharpenning_filter(
                input_image,
                alpha=float(self.argument1_value),
                filter_sigma=float(self.size)
            )
        elif self.filter_type == self.PERCENTILE:
            output_image = ndimage.percentile_filter(
                input_image,
                percentile=int(self.argument_1_value),
                size=int(self.size_value),
            )
        elif self.filter_type == self.WIENER:
            output_image = signal.wiener(
                input_image,
                mysize=int(self.size_value),  # TODO: Should be odd, add clean
                noise=float(self.argument1_value),
            )
        elif self.filter_type == self.SOBEL:
            output_image = self.sobel_filter(
                input_image
            )

        # Save the result
        output_image = output_image.astype(input_image.dtype)
        imageio.imwrite(complete_file_name, output_image)
        return output_image

        def __str__(self):
            return _("Filter {} ({}: {}, Size: {})").format(
                self.get_filter_type_display(),
                self.argument1_name,
                self.argument1_value,
                self.size_value,
            )
