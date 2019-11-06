from PIL import Image

from django.db import models

from django.template.defaultfilters import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model

import numpy as np  # Image manipulation as nparray
from scipy import misc  # Open images


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

    def __str__(self):
        return self.name


class ItensityImageModifier(models.Model):
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
        POWER: _("fator"),
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

    def insert_uniform_noise(input_image, low=0, high=80, amount=1.0):
        return (
            input_image +
            amount * np.random.uniform(
                low, high,
                input_image.shape
            )
        )

    def insert_gaussian_noise(input_image, mean=5, std=30, amount=1.0):
        return (
            input_image +
            amount * np.random.normal(
                mean, std,
                input_image.shape
            )
        )

    def insert_rayleight_noise(input_image, scale=20, amount=1.0):
        return (
            input_image +
            amount * np.random.rayleigh(
                scale,
                input_image.shape
            )
        )

    def insert_exponential_noise(input_image, scale=5, amount=1.0):
        return (
            input_image +
            amount * np.random.exponential(
                scale,
                input_image.shape
            )
        )

    def insert_gamma_noise(input_image, shape=1, scale=8, amount=1.0):
        return (
            input_image +
            amount * np.random.gamma(
                shape, scale,
                input_image.shape
            )
        )

    def insert_salt_and_pepper_noise(input_image, s_vs_p=0.5, amount=0.004):
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

    def insert_noise(self, input_image, *args, **kwargs):
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
        if self.noise_type == 'uniform':
            output_image = self.insert_uniform_noise(
                input_image,
                *args,
                **kwargs
            )
        elif self.noise_type == 'gaussian':
            output_image = self.insert_gaussian_noise(
                input_image,
                *args,
                **kwargs
            )
        elif self.noise_type == 'rayleight':
            output_image = self.insert_rayleight_noise(
                input_image,
                *args,
                **kwargs
            )
        elif self.noise_type == 'exponential':
            output_image = self.insert_exponential_noise(
                input_image,
                *args,
                **kwargs
            )
        elif self.noise_type == 'gamma':
            output_image = self.insert_gamma_noise(
                input_image,
                *args,
                **kwargs
            )
        elif self.noise_type == 'salt_and_pepper':
            output_image = self.insert_salt_and_pepper_noise(
                input_image,
                *args,
                **kwargs
            )

        output_image = output_image.astype(input_image.dtype)  # input format
        return output_image

    def apply_modifier(self, input_image):
        complete_file_name = self.image.edited_image.path
        # Open the image file
        input_image = misc.imread(complete_file_name)
        # Apply the Modifier
        arguments = {
            self.argument1_name: self.argument1_value,
            self.argument2_name: self.argument2_value,
            'amount': self.amount_value,
        }
        output_image = self.insert_noise(input_image, **arguments)
        # Save the result
        misc.imsave(complete_file_name, output_image)


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

    def insert_uniform_noise(input_image, low=0, high=80, amount=1.0):
        return (
            input_image +
            amount * np.random.uniform(
                low, high,
                input_image.shape
            )
        )

    def insert_gaussian_noise(input_image, mean=5, std=30, amount=1.0):
        return (
            input_image +
            amount * np.random.normal(
                mean, std,
                input_image.shape
            )
        )

    def insert_rayleight_noise(input_image, scale=20, amount=1.0):
        return (
            input_image +
            amount * np.random.rayleigh(
                scale,
                input_image.shape
            )
        )

    def insert_exponential_noise(input_image, scale=5, amount=1.0):
        return (
            input_image +
            amount * np.random.exponential(
                scale,
                input_image.shape
            )
        )

    def insert_gamma_noise(input_image, shape=1, scale=8, amount=1.0):
        return (
            input_image +
            amount * np.random.gamma(
                shape, scale,
                input_image.shape
            )
        )

    def insert_salt_and_pepper_noise(input_image, s_vs_p=0.5, amount=0.004):
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

    def insert_noise(self, input_image, *args, **kwargs):
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
        if self.noise_type == 'uniform':
            output_image = self.insert_uniform_noise(
                input_image,
                *args,
                **kwargs
            )
        elif self.noise_type == 'gaussian':
            output_image = self.insert_gaussian_noise(
                input_image,
                *args,
                **kwargs
            )
        elif self.noise_type == 'rayleight':
            output_image = self.insert_rayleight_noise(
                input_image,
                *args,
                **kwargs
            )
        elif self.noise_type == 'exponential':
            output_image = self.insert_exponential_noise(
                input_image,
                *args,
                **kwargs
            )
        elif self.noise_type == 'gamma':
            output_image = self.insert_gamma_noise(
                input_image,
                *args,
                **kwargs
            )
        elif self.noise_type == 'salt_and_pepper':
            output_image = self.insert_salt_and_pepper_noise(
                input_image,
                *args,
                **kwargs
            )

        output_image = output_image.astype(input_image.dtype)  # input format
        return output_image

    def apply_modifier(self, input_image):
        complete_file_name = self.image.edited_image.path
        # Open the image file
        input_image = misc.imread(complete_file_name)
        # Apply the Modifier
        arguments = {
            self.argument1_name: self.argument1_value,
            self.argument2_name: self.argument2_value,
            'amount': self.amount_value,
        }
        output_image = self.insert_noise(input_image, **arguments)
        # Save the result
        misc.imsave(complete_file_name, output_image)
