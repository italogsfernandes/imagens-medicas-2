from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

class MedicalImage(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(blank=True, default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(
        unique=True, verbose_name=_("Slug"), null=True, blank=True
    )
    name = models.CharField(max_length=255)
    description_text = models.TextField(blank=True, default='')

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(MedicalImage, self).clean()

    def __str__(self):
        return self.name
