# # -*- coding: utf-8 -*-
# """Contains free-floating functions for interacting with PyPI."""
# # import json
# import logging

# # from dateutil.parser import parse
# import requests
# from semantic_version import Version
# # import semantic_version

# logger = logging.getLogger(__name__)


# def package_url(package_name):
#     """Return fully-qualified URL to package on PyPI (JSON endpoint)."""
#     return u"http://pypi.python.org/pypi/%s/json" % package_name


# def package_data(package_url):
#     """Return info, releases from PyPI package.

#     Args:
#         package_url: string, the name of the package on PyPI.

#     Returns a 3-tuple containing info (dict), releases (dict), versions (list of
#         PackageVersion objects parsed from releases JSON).

#     """
#     data = requests.get(package_url).json()
#     info = data.get('info')
#     releases = data.get('releases')
#     versions = parse_releases(releases)
#     licence, latest = parse_info(info)
#     return licence, latest, versions


# def next_version(current_version, all_versions):
#     """Return the next available version, else None if up-to-date."""
#     try:
#         return min([v for v in all_versions if v > current_version])
#     except ValueError:
#         return None

# # def package_json(package_url):
# #     """Return the complete package descriptor from PyPI.

# #     Includes latest version info and releases.

# #     """
# #     return requests.get(package_url).json()


# # def package_info(package_data):
# #     """Return latest package version from PyPI (as JSON).

# #     Returns a JSON object containing the output from the PyPI API.

# #     """
# #     return package_data.get('info')


# # def package_release_versions(package_releases):
# #     """Convert releases dict into list of valid semver versions.

# #     This is an example from Django of the releases JSON block. Some releases have
# #     no detail, some have more than one. Working out which version is available is
# #     therefore more complicated that just matching release numbers.

# #     In order to determine the *next* release, we look at all releases with an
# #     upload_time and ignore all others. For those with two dates, we take the
# #     later of the two.

# #     "releases": {
# #         "1.0.4": [],
# #         "1.0.1": [],
# #         "1.0.2": [],
# #         "1.0.3": [],
# #         "1.6.10": [
# #             {
# #                 "has_sig": true,
# #                 "upload_time": "2015-01-13T18:48:42",
# #                 "comment_text": "",
# #                 "python_version": "py2.py3",
# #                 "url": "https://pypi.python.org/packages/py2.py3/D/Django/Django-1.6.10-py2.py3-none-any.whl",
# #                 "md5_digest": "f83dcaec9e3b7d956a4d29e9401b0b97",
# #                 "downloads": 174250,
# #                 "filename": "Django-1.6.10-py2.py3-none-any.whl",
# #                 "packagetype": "bdist_wheel",
# #                 "path": "py2.py3/D/Django/Django-1.6.10-py2.py3-none-any.whl",
# #                 "size": 6688308
# #             },
# #             {
# #                 "has_sig": true,
# #                 "upload_time": "2015-01-13T18:48:53",
# #                 "comment_text": "",
# #                 "python_version": "source",
# #                 "url": "https://pypi.python.org/packages/source/D/Django/Django-1.6.10.tar.gz",
# #                 "md5_digest": "d7123f14ac19ae001be02ed841937b91",
# #                 "downloads": 39317,
# #                 "filename": "Django-1.6.10.tar.gz",
# #                 "packagetype": "sdist",
# #                 "path": "source/D/Django/Django-1.6.10.tar.gz",
# #                 "size": 6760152
# #             }
# #         ],
# #     }

# #     """
# #     logger.debug("Fetching package releases from %s", package_url)
# #     releases = package_data.get('releases')
# #     return releases


# # def package_version(release_data):
# #     """Return the latest version from package_version as semver Version."""
# #     return semantic_version.Version.coerce(package_info.get('version'))


# def parse_version(version_string):
#     """Parse a string into a PackageVersion."""
#     try:
#         return Version.coerce(version_string)
#     except:
#         return None


# def parse_releases(releases):
#     """Return ordered list of all parseable PackageVersion objects.

#     Args:
#         releases: dictionary parsed from the package_url - each key is
#             a version string, which is parsed out into a PackageVersion.

#     Returns a list of all the releases parsed into PackageVersion, sorted
#         in package order, with null packages (unparseable) removed.

#     """
#     versions = [parse_version(r) for r in releases.keys()]
#     return sorted([v for v in versions if v is not None])


# def parse_info(info):
#     """Return the licence and latest version from the info JSON."""
#     licence = info.get('license', '(unspecified)')[:100]
#     version = parse_version(info.get('version'))
#     return licence, version


# def version_diff(version1, version2):
#     """Return string representing the diff between package versions.

#     We're interested in whether this is a major, minor, patch or 'other'
#     update. This method will compare the two versions and return None if
#     they are the same, else it will return a string value indicating the
#     type of diff - 'major', 'minor', 'patch', 'other'.

#     Args:
#         version1: the Version object we are interested in (e.g. current)
#         version2: the Version object to compare against (e.g. latest)

#     Returns a string - 'major', 'minor', 'patch', 'other', or None if the
#         two are identical.

#     """
#     if version1 is None or version2 is None:
#         return 'unknown'
#     if version1 == version2:
#         return 'none'

#     for v in ('major', 'minor', 'patch'):
#         if getattr(version1, v) != getattr(version2, v):
#             return v

#     return 'other'
