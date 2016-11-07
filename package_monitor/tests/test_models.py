# -*- coding: utf-8 -*-
from django.test import TestCase

from mock import patch
from requirements import requirement
from semantic_version import Version

from .. import models
from ..tests import mock_get


class PackageVersionTests(TestCase):

    """PackageVersion model tests."""

    def test_attrs(self):
        v = models.PackageVersion()
        self.assertEqual(v.raw, '')
        self.assertEqual(v.package_name, '')
        self.assertEqual(v.current_version, None)
        self.assertEqual(v.latest_version, None)
        self.assertEqual(v.licence, '')
        self.assertEqual(v.diff_status, 'unknown')
        self.assertEqual(v.checked_pypi_at, None)
        self.assertEqual(v.is_editable, False)
        self.assertEqual(v.is_parseable, False)
        self.assertEqual(v.url, None)

        v.save()
        self.assertEqual(v.raw, '')
        self.assertEqual(v.package_name, '')
        self.assertEqual(v.current_version, None)
        self.assertEqual(v.latest_version, None)
        self.assertEqual(v.licence, '')
        self.assertEqual(v.diff_status, 'unknown')
        self.assertEqual(v.checked_pypi_at, None)
        self.assertEqual(v.is_editable, False)
        self.assertEqual(v.is_parseable, False)
        self.assertEqual(v.url, None)

        v.raw = 'foobar==1.2'
        self.assertEqual(unicode(v), u"Package 'foobar==1.2'")
        self.assertEqual(str(v), u"Package 'foobar==1.2'")

    def test_init(self):
        r = requirement.Requirement.parse("foobar==0.0.1")
        v = models.PackageVersion(requirement=r)
        self.assertEqual(v.package_name, 'foobar')
        self.assertEqual(v.raw, 'foobar==0.0.1')
        self.assertEqual(v.current_version, Version('0.0.1'))
        self.assertEqual(v.latest_version, None)
        self.assertEqual(v.licence, '')
        self.assertEqual(v.diff_status, 'unknown')
        self.assertEqual(v.checked_pypi_at, None)
        self.assertEqual(v.is_editable, False)
        self.assertEqual(v.url, u"http://pypi.python.org/pypi/foobar/json")

    def test_init_editable(self):
        url = "git+https://foobar.com#egg=foo"
        r = requirement.Requirement.parse("-e " + url)
        v = models.PackageVersion(requirement=r)
        self.assertEqual(v.package_name, 'foo')
        self.assertEqual(v.raw, '-e ' + url)
        self.assertEqual(v.current_version, None)
        self.assertEqual(v.latest_version, None)
        self.assertEqual(v.licence, '')
        self.assertEqual(v.diff_status, 'unknown')
        self.assertEqual(v.checked_pypi_at, None)
        self.assertEqual(v.is_editable, True)
        self.assertEqual(v.url, '')

    def test_init_unparseable(self):
        r = requirement.Requirement.parse("foo==0.01.0")
        v = models.PackageVersion(requirement=r)
        self.assertEqual(v.package_name, 'foo')
        self.assertEqual(v.current_version, None)
        self.assertEqual(v.latest_version, None)
        self.assertEqual(v.licence, '')
        self.assertEqual(v.diff_status, 'unknown')
        self.assertEqual(v.checked_pypi_at, None)
        self.assertEqual(v.is_editable, False)
        self.assertEqual(v.is_editable, False)
        self.assertEqual(v.url, u'http://pypi.python.org/pypi/foo/json')

    @patch('requests.get', mock_get)
    def test_update_from_pypi(self):
        """Test the update_from_pypi method."""
        # editable packages return None
        r = requirement.Requirement.parse("foobar==0.0.1")
        v = models.PackageVersion(requirement=r)
        v.update_from_pypi()
        self.assertEqual(v.licence, 'BSD')
        self.assertEqual(v.current_version, Version('0.0.1'))
        self.assertEqual(v.latest_version, Version('1.9.1'))
        self.assertEqual(v.diff_status, 'major')

    @patch('requests.get', mock_get)
    def test_update_from_pypi_unparseable(self):
        """Test the update_from_pypi method for unparseable requirements."""
        # editable packages return None
        r = requirement.Requirement.parse("foobar==0.00.1")
        v = models.PackageVersion(requirement=r)
        v.update_from_pypi()
        self.assertEqual(v.licence, 'BSD')
        self.assertEqual(v.current_version, None)
        self.assertEqual(v.latest_version, None)
        self.assertEqual(v.diff_status, 'unknown')
