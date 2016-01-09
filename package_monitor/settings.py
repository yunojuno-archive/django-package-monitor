# -*- coding: utf-8 -*-
"""package_monitor app settings."""
from os import path, getenv

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

REQUIREMENTS_FILE = (
    getattr(settings, 'PACKAGE_MONITOR_REQUIREMENTS_FILE', None) or
    getenv('PACKAGE_MONITOR_REQUIREMENTS_FILE', None)
)

if REQUIREMENTS_FILE is None:
    raise ImproperlyConfigured('Missing PACKAGE_MONITOR_REQUIREMENTS_FILE setting.')

if not path.exists(REQUIREMENTS_FILE):
    raise ImproperlyConfigured('Invalid REQUIREMENTS_FILE setting: %s' % REQUIREMENTS_FILE)


# length of time to cache return data from PyPI
PYPI_CACHE_EXPIRY = getattr(settings, 'PACKAGE_MONITOR_PYPI_CACHE_EXPIRY', 30)
