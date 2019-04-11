from os.path import join

from .base import *  # NOQA

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!-mi(aqg))3348d$%g0e%plgxtrgl5#m!3a-e3h9vmwuz%(r6i'

DATABASES['default']['USER'] = 'http'  # NOQA


ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'italogsfernandes.com',
]

try:
    from .local import *  # NOQA
except ImportError:
    pass
