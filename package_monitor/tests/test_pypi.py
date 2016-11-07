# -*- coding: utf-8 -*-
"""Tests for the pypi module."""
import json
import mock
from os import path

from django.core.cache import cache
from django.test import TestCase

from semantic_version import Version

from .. import pypi


def mock_get(packge_url):
    """Mock for requests.get function."""
    class response(object):

        def test_data_path(self, filename):
            return path.join(
                path.abspath(path.dirname(__file__)),
                'test_data/%s.json' % filename
            )

        def json(self):
            with open(self.test_data_path('pypi_django'), 'r') as django:
                return json.load(django)

    return response()


class FunctionTests(TestCase):

    """Free floating function tests."""

    def setUp(self):
        self.v_0_0_1 = Version('0.0.1')
        self.v_0_0_2 = Version('0.0.2')
        self.v_0_1_0 = Version('0.1.0')
        self.v_1_0_0 = Version('1.0.0')
        self.v_other = Version('1.0.0-other')

    def test_version_diff(self):
        self.assertEqual(pypi.version_diff(None, None), 'unknown')
        self.assertEqual(pypi.version_diff(None, self.v_0_0_1), 'unknown')
        self.assertEqual(pypi.version_diff(self.v_0_0_1, None), 'unknown')
        self.assertEqual(pypi.version_diff(self.v_0_0_1, self.v_0_1_0), 'minor')

        self.assertEqual(pypi.version_diff(self.v_0_0_1, self.v_0_0_1), 'none')
        self.assertEqual(pypi.version_diff(self.v_0_0_1, self.v_0_0_2), 'patch')
        self.assertEqual(pypi.version_diff(self.v_0_0_1, self.v_0_1_0), 'minor')
        self.assertEqual(pypi.version_diff(self.v_0_0_1, self.v_1_0_0), 'major')

        self.assertEqual(pypi.version_diff(self.v_0_0_2, self.v_0_0_1), 'patch')
        self.assertEqual(pypi.version_diff(self.v_0_0_2, self.v_0_0_2), 'none')
        self.assertEqual(pypi.version_diff(self.v_0_0_2, self.v_0_1_0), 'minor')
        self.assertEqual(pypi.version_diff(self.v_0_0_2, self.v_1_0_0), 'major')

        self.assertEqual(pypi.version_diff(self.v_0_1_0, self.v_0_0_1), 'minor')
        self.assertEqual(pypi.version_diff(self.v_0_1_0, self.v_0_0_2), 'minor')
        self.assertEqual(pypi.version_diff(self.v_0_1_0, self.v_0_1_0), 'none')
        self.assertEqual(pypi.version_diff(self.v_0_1_0, self.v_1_0_0), 'major')

        self.assertEqual(pypi.version_diff(self.v_1_0_0, self.v_0_0_1), 'major')
        self.assertEqual(pypi.version_diff(self.v_1_0_0, self.v_0_0_2), 'major')
        self.assertEqual(pypi.version_diff(self.v_1_0_0, self.v_0_1_0), 'major')
        self.assertEqual(pypi.version_diff(self.v_1_0_0, self.v_1_0_0), 'none')

        self.assertEqual(pypi.version_diff(self.v_1_0_0, self.v_other), 'other')

    def test_parse_version(self):
        self.assertEqual(pypi.parse_version('1.0.0'), Version('1.0.0'))
        self.assertEqual(pypi.parse_version("foobar"), None)

    def test_package_url(self):
        self.assertEqual(pypi.package_url('django'), u"http://pypi.python.org/pypi/django/json")


class PackageTests(TestCase):

    """Tests for parsing PyPI package data - NB uses static data."""

    def setUp(self):
        # with mock.patch('requests.get', mock_get):
        self.package = pypi.Package('django')
        self.test_data = mock_get('foo').json()

    def test_url(self):
        self.assertEqual(self.package.url, pypi.package_url('django'))

    @mock.patch('requests.get', mock_get)
    def test_data_caching(self):
        cache.clear()
        key = pypi.cache_key('django')
        package = pypi.Package('django')
        self.assertIsNone(cache.get(key))
        self.assertEqual(package.data(), self.test_data)
        self.assertEqual(cache.get(key), self.package.data())

    @mock.patch('requests.get', mock_get)
    def test_data(self):
        self.assertEqual(self.package.data(), self.test_data)

    @mock.patch('requests.get', mock_get)
    def test_info(self):
        self.assertEqual(self.package.info(), self.test_data['info'])

    @mock.patch('requests.get', mock_get)
    def test_licence(self):
        self.assertEqual(self.package.licence(), self.test_data['info']['license'])
        self.assertEqual(self.package.licence(), 'BSD')

    @mock.patch('requests.get', mock_get)
    def test_latest_version(self):
        self.assertEqual(self.package.latest_version(), Version('1.9.1'))

    @mock.patch('requests.get', mock_get)
    def test_all_versions(self):
        all_versions = self.package.all_versions()
        self.assertEqual(len(all_versions), 104)
        self.assertEqual(Version('1.0.1'), all_versions[0])
        self.assertEqual(Version('1.9.1'), all_versions[-1])

    @mock.patch('requests.get', mock_get)
    def test_next_version(self):
        self.assertEqual(self.package.next_version(Version('0.0.1')), Version('1.0.1'))
        self.assertEqual(self.package.next_version(Version('1.0.0')), Version('1.0.1'))
        self.assertEqual(self.package.next_version(Version('1.9.1')), None)
