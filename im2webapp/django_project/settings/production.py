import os
from .base import *  # NOQA

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_IM2WEBAPP_PRODUCTION_SECRET_KEY')

# DATABASES['default']['USER'] = 'http'  # NOQA


ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'italogsfernandes.com',
]

try:
    from .local import *  # NOQA
except ImportError:
    pass
