from PIL import Image

from django.db import models

from django.template.defaultfilters import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model

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
