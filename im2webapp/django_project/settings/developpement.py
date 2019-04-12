import os
from .base import *  # NOQA

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'italogsfernandes.com',
]

for template_engine in TEMPLATES:  # NOQA
    template_engine['OPTIONS']['debug'] = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_IM2WEBAPP_DEVELOPPEMENT_SECRET_KEY')

try:
    from .local import *  # NOQA
except ImportError:
    pass
