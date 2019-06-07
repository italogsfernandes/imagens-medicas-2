import os
from .base import *  # NOQA

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_IM2WEBAPP_PRODUCTION_SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'im2webapp',
        'USER': os.environ.get('DJANGO_IM2WEBAPP_PRODUCTION_POSTGRESQL_USER'),
        'PASSWORD': os.environ.get(
            'DJANGO_IM2WEBAPP_PRODUCTION_POSTGRESQL_PASSWORD'),
        'HOST': os.environ.get('DJANGO_IM2WEBAPP_PRODUCTION_POSTGRESQL_HOST'),
        'PORT': os.environ.get('DJANGO_IM2WEBAPP_PRODUCTION_POSTGRESQL_PORT'),
    }
}


ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'italogsfernandes.com',
]

try:
    from .local import *  # NOQA
except ImportError:
    pass
