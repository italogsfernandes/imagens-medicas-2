import os
from .developpement import *  # NOQA

SECRET_KEY = os.environ.get('DJANGO_IM2WEBAPP_TESTS_SECRET_KEY')
DEBUG = False
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'im2webapp_test',
    }
}
