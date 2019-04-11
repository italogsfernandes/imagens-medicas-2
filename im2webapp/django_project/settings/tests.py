from os.path import join

from .developpement import *  # NOQA

SECRET_KEY = "57c%giio-i327pa+c*w5)^$hpemx35s@c3*2%ncgu9fp#pxc9r"
DEBUG = False
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'travis_ci_db',
        'USER': 'travis',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
    }
}
