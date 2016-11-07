# -*- coding: utf-8 -*-
"""Contains free-floating functions for interacting with PyPI."""
import logging

import requests
from semantic_version import Version

from django.core.cache import cache

from .settings import PYPI_CACHE_EXPIRY


logger = logging.getLogger(__name__)


def cache_key(package_name):
    """Return cache key for a package."""
    return "package_monitor.cache:%s" % package_name


def package_url(package_name):
    """Return fully-qualified URL to package on PyPI (JSON endpoint)."""
    return u"http://pypi.python.org/pypi/%s/json" % package_name


def parse_version(version_string):
    """Parse a string into a PackageVersion."""
    try:
        return Version.coerce(version_string)
    except:
        return None


def version_diff(version1, version2):
    """Return string representing the diff between package versions.

    We're interested in whether this is a major, minor, patch or 'other'
    update. This method will compare the two versions and return None if
    they are the same, else it will return a string value indicating the
    type of diff - 'major', 'minor', 'patch', 'other'.

    Args:
        version1: the Version object we are interested in (e.g. current)
        version2: the Version object to compare against (e.g. latest)

    Returns a string - 'major', 'minor', 'patch', 'other', or None if the
        two are identical.

    """
    if version1 is None or version2 is None:
        return 'unknown'
    if version1 == version2:
        return 'none'

    for v in ('major', 'minor', 'patch'):
        if getattr(version1, v) != getattr(version2, v):
            return v

    return 'other'


class Package(object):

    """Package class models the PyPI JSON for a package."""

    def __init__(self, package_name):
        self.name = package_name

    @property
    def url(self):
        return package_url(self.name)

    def data(self):
        """Fetch latest data from PyPI, and cache for 30s."""
        key = cache_key(self.name)
        data = cache.get(key)
        if data is None:
            logger.debug("Updating package info for %s from PyPI.", self.name)
            data = requests.get(self.url).json()
            cache.set(key, data, PYPI_CACHE_EXPIRY)
        return data

    def info(self):
        return self.data().get('info')

    def licence(self):
        return self.info().get('license') or '(unspecified)'

    def latest_version(self):
        return parse_version(self.info().get('version'))

    def all_versions(self):
        release_data = self.data().get('releases')
        versions = [parse_version(r) for r in release_data.keys()]
        return sorted([v for v in versions if v is not None])

    def next_version(self, current_version):
        try:
            return min([v for v in self.all_versions() if v > current_version])
        except ValueError:
            return None
