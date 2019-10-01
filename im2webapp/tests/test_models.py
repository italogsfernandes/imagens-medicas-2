from mixer.backend.django import mixer
import pytest

from django.template.defaultfilters import slugify


@pytest.mark.django_db
class TestModels:
    def test_image_model_str(self):
        image = mixer.blend('im2webapp.ImageModel')
        assert str(image) == image.name

    def test_image_model_clean(self):
        image = mixer.blend('im2webapp.ImageModel')
        image.clean()
        assert image.slug == slugify(image.name)
