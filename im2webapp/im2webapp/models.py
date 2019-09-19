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

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)
            return super(ImageModel, self).clean()

    def __str__(self):
        return self.name


class SimpleImageModifier(models.Model):
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


    def apply(self):
        pass
