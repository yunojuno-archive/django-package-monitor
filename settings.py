# -*- coding: utf-8 -*-
from os import getenv, path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# You should really update this in your app!
# see https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = getenv('ALLOWED_HOSTS', '*')

USE_L10N = True
USE_I18N = True
USE_TZ = True
TIMEZONE = 'Europe/London'

EMAIL_HOST = getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = getenv('EMAIL_PORT', '25')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'package_monitor.db',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'package_monitor',
)

MIDDLEWARE_CLASSES = [
    # default django middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

PROJECT_ROOT = path.realpath(path.dirname(__file__))

STATIC_URL = "/static/"

SECRET_KEY = "secret"

# requests can be really noisy, and it uses a bunch of different
# loggers, so use this to turn all requests-related loggers down
REQUESTS_LOGGING_LEVEL = getenv('REQUESTS_LOGGING_LEVEL', 'WARNING')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'INFO',
        },
        'package_monitor': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'requests': {
            'handlers': ['console'],
            'level': REQUESTS_LOGGING_LEVEL,
            'propagate': False,
        },
        'urllib3': {
            'handlers': ['console'],
            'level': REQUESTS_LOGGING_LEVEL,
            'propagate': False,
        },
        'oauthlib': {
            'handlers': ['console'],
            'level': REQUESTS_LOGGING_LEVEL,
            'propagate': False,
        },
        'requests_oauthlib': {
            'handlers': ['console'],
            'level': REQUESTS_LOGGING_LEVEL,
            'propagate': False,
        },
    }
}

ROOT_URLCONF = 'urls'

APPEND_SLASH = True

assert DEBUG is True, "This project is only intended to be used for testing."

# == package_monitor settings ==
PACKAGE_MONITOR_REQUIREMENTS_FILE = path.join(PROJECT_ROOT, 'requirements.txt')
