from mixer.backend.django import mixer
import pytest

from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.templatetags.static import static
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestModels:
    def test_image_model_str(self):
        image = mixer.blend('im2webapp.ImageModel')
        assert str(image) == image.name

    def test_image_model_clean(self):
        image = mixer.blend('im2webapp.ImageModel')
        image.clean()
        assert image.slug == slugify(image.name)

        image = mixer.blend('im2webapp.ImageModel')
        image.slug = "hello_there"
        image.clean()
        assert image.slug == 'hello_there'


@pytest.mark.django_db
class TestUserModels:
    def test_profile_str(self):
        user = mixer.blend(User)
        profile = user.profile
        assert str(profile) == '{} Profile'.format(profile.user.username)

    def test_profile_save(self):
        user = mixer.blend(User)
        profile = user.profile
        infile = open(
            'im2webapp' + static('im2webapp/images/examples/simulated.bmp'),
            'rb'
        )
        profile_image = SimpleUploadedFile(
            static('im2webapp/images/examples/simulated.bmp'),
            infile.read(),
        )
        infile.close()

        profile.image = profile_image
        profile.save()

        img = Image.open(profile.image.path)
        assert img.height <= 300
        assert img.width <= 300
