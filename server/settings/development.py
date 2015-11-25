from os.path import join


from common import *


DEBUG = True

sys.path.append(normpath(join(PROJECT_ROOT, 'apps')))


DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': join(PROJECT_ROOT, 'run', 'dev.sqlite3'),
    }
