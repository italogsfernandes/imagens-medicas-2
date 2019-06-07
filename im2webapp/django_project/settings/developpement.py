import os
from .base import *  # NOQA

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if os.environ.get('DJANGO_IM2WEBAPP_PRODUCTION_POSTGRESQL_PASSWORD'):
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

for template_engine in TEMPLATES:  # NOQA
    template_engine['OPTIONS']['debug'] = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_IM2WEBAPP_DEVELOPPEMENT_SECRET_KEY',
    'lrqa@71ktxw8rgkm&w9w41w4s5bxvn83+qxdzdggt6z=8qrgkz',  # Default value
)

try:
    from .local import *  # NOQA
except ImportError:
    pass
