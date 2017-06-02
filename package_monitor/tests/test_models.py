# -*- coding: utf-8 -*-
from django.test import TestCase

from requirements import requirement
from semantic_version import Version

from .. import models
from ..compat import mock
from ..tests import mock_get

# valid line from a pip-compile generated requirements.txt
SAMPLE_LINE = (
    "six==1.10.0               # via apscheduler, bleach, django-appmail, "
    "django-rosetta, elasticsearch-dsl, html5lib, microsofttranslator, "
    "python-dateutil, python-memcached, social-auth-app-django, social-auth-core, twilio"
)


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
        self.assertEqual(str(v), "Package 'foobar==1.2'")

    def test_init(self):
        r = requirement.Requirement.parse(SAMPLE_LINE)
        v = models.PackageVersion(requirement=r)
        self.assertEqual(v.package_name, 'six')
        self.assertEqual(v.raw, SAMPLE_LINE)
        self.assertEqual(v.current_version, Version('1.10.0'))
        self.assertEqual(v.latest_version, None)
        self.assertEqual(v.licence, '')
        self.assertEqual(v.diff_status, 'unknown')
        self.assertEqual(v.checked_pypi_at, None)
        self.assertEqual(v.is_editable, False)
        self.assertEqual(v.url, "http://pypi.python.org/pypi/six/json")

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
        self.assertEqual(v.url, 'http://pypi.python.org/pypi/foo/json')

    @mock.patch('requests.get', mock_get)
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

    @mock.patch('requests.get', mock_get)
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

    def test_save(self):
        v = models.PackageVersion(raw=SAMPLE_LINE)
        v1 = v.save()
        self.assertEqual(v1, v)
        self.assertNotEqual(v.raw, SAMPLE_LINE)
        self.assertEqual(v.raw, SAMPLE_LINE[:200])
