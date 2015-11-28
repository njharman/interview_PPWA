import sys
from os.path import abspath, basename, dirname, join, normpath


## Settings that are shared and safe to have in dev, test, and production.
## Imported by other settings file.

DEBUG = False

ADMINS = (
    ('Norman Harman', 'njharman@gmail.com'),
    )
MANAGERS = ADMINS

PRODUCT_API_URL = 'https://careers.undercovertourist.com/assignment/1/products/'
PRODUCT_API_AUTH = 'first.last'

SITE_ID = 1
SITE_NAME = 'server'
ROOT_URLCONF = '%s.urls' % SITE_NAME
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME

DJANGO_ROOT = dirname(dirname(abspath(__file__)))
PROJECT_ROOT = dirname(DJANGO_ROOT)

MEDIA_URL = '/media/'
MEDIA_ROOT = join(PROJECT_ROOT, 'run', 'media')

STATIC_URL = '/static/'
STATIC_ROOT = join(PROJECT_ROOT, 'run', 'static')
STATICFILES_DIRS = [
    join(PROJECT_ROOT, SITE_NAME, 'static'),
    ]

PROJECT_TEMPLATES = [
    join(PROJECT_ROOT, SITE_NAME, 'templates'),
    ]

DATABASES = {}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'ppwa',
    ]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    ]

TEMPLATES = [
    {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': PROJECT_TEMPLATES,
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': join(PROJECT_ROOT, 'run', 'django.log')
            },
         'console': {
            'class': 'logging.StreamHandler',
            },
        },
    'loggers': {
        'ppwa': {
            'handlers': ['console'],
            'level': 'INFO',
            },
        'ppwa.command': {
            'level': 'DEBUG',
            'propagate': True,
            },
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
            },
        },
    }

LANGUAGE_CODE = 'en'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# We store the secret key here and fetch it.
SECRET_FILE = normpath(join(PROJECT_ROOT, 'run', 'SECRET.key'))

try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        from django.utils.crypto import get_random_string
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!$%&()=+-_'
        SECRET_KEY = get_random_string(50, chars)
        with open(SECRET_FILE, 'w') as f:
            f.write(SECRET_KEY)
    except IOError:
        raise Exception('Could not open %s for writing!' % SECRET_FILE)
