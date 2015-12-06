# -*- coding: utf-8 -*-
"""Contains free-floating functions for interacting with PyPI."""
import logging

import requests
import semantic_version

logger = logging.getLogger(__name__)


def package_url(package):
    """Return fully-qualified URL to package on PyPI (JSON endpoint)."""
    return u"http://pypi.python.org/pypi/%s/json" % package


def package_info(package_url):
    """Return latest package version from PyPI (as JSON).

    Returns a JSON object containing the output from the PyPI API.

    """
    logger.debug("Fetching package info from %s", package_url)
    return requests.get(package_url).json().get('info')


def package_version(package_info):
    """Return the latest version from package_version as semver Version."""
    return semantic_version.Version.coerce(package_info.get('version'))


def package_licence(package_info):
    """Return the licence from info JSON (truncated to 100 chars)."""
    licence = package_info.get('license') or ''
    return licence[:100]


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
