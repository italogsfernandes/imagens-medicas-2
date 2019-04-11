from .base import *  # NOQA

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

for template_engine in TEMPLATES:  # NOQA
    template_engine['OPTIONS']['debug'] = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!-mi(aqg))3348d$%g0e%plgxtrgl5#m!3a-e3h9vmwuz%(r6i'

try:
    from .local import *  # NOQA
except ImportError:
    pass
