import logging
from typing import Any, Dict, Iterable, List, Optional

import requests
from django.core.cache import cache
from semantic_version import Version

from .settings import PYPI_CACHE_EXPIRY

logger = logging.getLogger(__name__)


def cache_key(package_name: str) -> str:
    """Return cache key for a package."""
    return "package_monitor.cache:%s" % package_name


def package_url(package_name: str) -> str:
    """Return fully-qualified URL to package on PyPI (JSON endpoint)."""
    return "https://pypi.python.org/pypi/%s/json" % package_name


def parse_version(version_string: Optional[str]) -> Optional[Version]:
    """Parse a string into a PackageVersion."""
    try:
        return Version.coerce(version_string)
    except Exception:
        return None


def parse_python(classifiers: Iterable[str]) -> str:
    """Parse out the versions of python supported a/c classifiers."""
    prefix = "Programming Language :: Python ::"
    python_classifiers = [
        c.split("::")[2].strip() for c in classifiers if c.startswith(prefix)
    ]
    return ", ".join([c for c in python_classifiers if parse_version(c)])


def parse_django(classifiers: Iterable) -> str:
    """Parse out the versions of django supported a/c classifiers."""
    prefix = "Framework :: Django ::"
    django_classifiers = [
        c.split("::")[2].strip() for c in classifiers if c.startswith(prefix)
    ]
    return ", ".join([c for c in django_classifiers if parse_version(c)])


def version_diff(version1: Optional[Version], version2: Optional[Version]) -> str:
    """
    Return string representing the diff between package versions.

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
        return "unknown"
    if version1 == version2:
        return "none"

    for v in ("major", "minor", "patch"):
        if getattr(version1, v) != getattr(version2, v):
            return v

    return "other"


class Package(object):
    """Package class models the PyPI JSON for a package."""

    def __init__(self, package_name: str) -> None:
        self.name = package_name

    @property
    def url(self) -> str:
        return package_url(self.name)

    def data(self) -> dict:
        """Fetch latest data from PyPI, and cache for 30s."""
        key = cache_key(self.name)
        data = cache.get(key)
        if data is None:
            logger.debug("Updating package info for %s from PyPI.", self.name)
            data = requests.get(self.url).json()
            cache.set(key, data, PYPI_CACHE_EXPIRY)
        return data

    def info(self) -> Dict[str, Any]:
        return self.data().get("info", {})

    def licence(self) -> str:
        return self.info().get("license", "(unspecified)")

    def classifiers(self) -> List[str]:
        return self.info().get("classifiers", [])

    def latest_version(self) -> Optional[Version]:
        return parse_version(self.info().get("version"))

    def all_versions(self) -> List[Version]:
        release_data = self.data().get("releases")
        if not release_data:
            return []
        versions = [parse_version(r) for r in list(release_data.keys())]
        return sorted([v for v in versions if v is not None])

    def next_version(self, current_version: Version) -> Optional[Version]:
        try:
            return min([v for v in self.all_versions() if v > current_version])
        except ValueError:
            return None

    def python_support(self) -> str:
        return parse_python(self.classifiers())

    def django_support(self) -> str:
        return parse_django(self.classifiers())

    def supports_py3(self) -> Optional[bool]:
        if self.python_support() == "":
            return None
        else:
            versions = self.python_support().split(", ")
            return len([v for v in versions if v != "" and v[0] == "3"]) > 0
