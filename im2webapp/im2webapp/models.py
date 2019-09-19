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
