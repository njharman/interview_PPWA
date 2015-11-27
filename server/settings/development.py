from os.path import join


from common import *


DEBUG = True

PRODUCT_API_AUTH = 'norman.harman'

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': join(PROJECT_ROOT, 'run', 'dev.sqlite3'),
    }
