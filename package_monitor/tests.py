# # -*- coding: utf-8 -*-
# from django.test import TestCase

# from mock import patch
# from requirements import requirement
# from semantic_version import Version

# from package_monitor.pypi import
# from package_monitor import (
#     package_url,
#     package_info,
#     package_version,
#     package_licence,
#     version_diff,
#     models
# )

# TEST_INFO = {
#     'license': 'MIT',
#     'version': '1.0.0'
# }
# TEST_PYPI = {
#     'info': TEST_INFO
# }


# def mock_info(packge_url):
#     """Mock for package_info function."""
#     return TEST_INFO


# def mock_get(packge_url):
#     """Mock for requests.get function."""
#     class response(object):
#         def json(self):
#             return TEST_PYPI
#     return response()


# class FunctionTests(TestCase):

#     """Package function tests."""

#     @patch('package_monitor.models.package_info', mock_info)
#     @patch('requests.get', mock_get)
#     def test_version_diff(self):
#         self.assertEqual(package_url('foo'), u"http://pypi.python.org/pypi/foo/json")
#         self.assertEqual(package_info('foo'), TEST_INFO)
#         self.assertEqual(package_version(TEST_INFO), Version(TEST_INFO.get('version')))
#         self.assertEqual(package_licence(TEST_INFO), TEST_INFO.get('license'))

#     def test_package_licence(self):
#         self.assertEqual(package_licence({'license': None}), '')
#         self.assertEqual(package_licence({'license': "None"}), 'None')
#         self.assertEqual(package_licence({'license': "X" * 100}), "X" * 100)
#         self.assertEqual(package_licence({'license': "X" * 101}), "X" * 100)


# class VersionDiffTests(TestCase):

#     """Tests for the version_diff function."""

#     def setUp(self):
#         self.v_0_0_1 = Version('0.0.1')
#         self.v_0_0_2 = Version('0.0.2')
#         self.v_0_1_0 = Version('0.1.0')
#         self.v_1_0_0 = Version('1.0.0')
#         self.v_other = Version('1.0.0-other')

#     def test_version_diff(self):
#         self.assertEqual(version_diff(None, None), 'unknown')
#         self.assertEqual(version_diff(None, self.v_0_0_1), 'unknown')
#         self.assertEqual(version_diff(self.v_0_0_1, None), 'unknown')
#         self.assertEqual(version_diff(self.v_0_0_1, self.v_0_1_0), 'minor')

#         self.assertEqual(version_diff(self.v_0_0_1, self.v_0_0_1), 'none')
#         self.assertEqual(version_diff(self.v_0_0_1, self.v_0_0_2), 'patch')
#         self.assertEqual(version_diff(self.v_0_0_1, self.v_0_1_0), 'minor')
#         self.assertEqual(version_diff(self.v_0_0_1, self.v_1_0_0), 'major')

#         self.assertEqual(version_diff(self.v_0_0_2, self.v_0_0_1), 'patch')
#         self.assertEqual(version_diff(self.v_0_0_2, self.v_0_0_2), 'none')
#         self.assertEqual(version_diff(self.v_0_0_2, self.v_0_1_0), 'minor')
#         self.assertEqual(version_diff(self.v_0_0_2, self.v_1_0_0), 'major')

#         self.assertEqual(version_diff(self.v_0_1_0, self.v_0_0_1), 'minor')
#         self.assertEqual(version_diff(self.v_0_1_0, self.v_0_0_2), 'minor')
#         self.assertEqual(version_diff(self.v_0_1_0, self.v_0_1_0), 'none')
#         self.assertEqual(version_diff(self.v_0_1_0, self.v_1_0_0), 'major')

#         self.assertEqual(version_diff(self.v_1_0_0, self.v_0_0_1), 'major')
#         self.assertEqual(version_diff(self.v_1_0_0, self.v_0_0_2), 'major')
#         self.assertEqual(version_diff(self.v_1_0_0, self.v_0_1_0), 'major')
#         self.assertEqual(version_diff(self.v_1_0_0, self.v_1_0_0), 'none')

#         self.assertEqual(version_diff(self.v_1_0_0, self.v_other), 'other')


# class PackageVersionTests(TestCase):

#     """PackageVersion model tests."""

#     def test_attrs(self):
#         v = models.PackageVersion()
#         self.assertEqual(v.raw, '')
#         self.assertEqual(v.package_name, '')
#         self.assertEqual(v.current_version, None)
#         self.assertEqual(v.latest_version, None)
#         self.assertEqual(v.licence, '')
#         self.assertEqual(v.diff_status, 'unknown')
#         self.assertEqual(v.checked_pypi_at, None)
#         self.assertEqual(v.is_editable, False)
#         self.assertEqual(v.url, None)

#         v.save()
#         self.assertEqual(v.raw, '')
#         self.assertEqual(v.package_name, '')
#         self.assertEqual(v.current_version, None)
#         self.assertEqual(v.latest_version, None)
#         self.assertEqual(v.licence, '')
#         self.assertEqual(v.diff_status, 'unknown')
#         self.assertEqual(v.checked_pypi_at, None)
#         self.assertEqual(v.is_editable, False)
#         self.assertEqual(v.url, None)

#         v.raw = 'foobar==1.2'
#         self.assertEqual(unicode(v), u"Package 'foobar==1.2'")
#         self.assertEqual(str(v), u"Package 'foobar==1.2'")

#     def test_init(self):
#         r = requirement.Requirement.parse("foobar==0.0.1")
#         v = models.PackageVersion(requirement=r)
#         self.assertEqual(v.package_name, 'foobar')
#         self.assertEqual(v.raw, 'foobar==0.0.1')
#         self.assertEqual(v.current_version, Version('0.0.1'))
#         self.assertEqual(v.latest_version, None)
#         self.assertEqual(v.licence, '')
#         self.assertEqual(v.diff_status, 'unknown')
#         self.assertEqual(v.checked_pypi_at, None)
#         self.assertEqual(v.is_editable, False)
#         self.assertEqual(v.url, u"http://pypi.python.org/pypi/foobar/json")

#     @patch('package_monitor.models.package_info', mock_info)
#     def test_info(self):
#         """Test the get_info method."""
#         r = requirement.Requirement.parse("foobar==0.0.1")
#         v = models.PackageVersion(requirement=r)
#         self.assertEqual(v.is_editable, False)
#         self.assertEqual(v.get_info(), TEST_INFO)

#         # editable packages return None
#         r = requirement.Requirement.parse("-e foobar==0.0.1")
#         v = models.PackageVersion(requirement=r)
#         self.assertEqual(v.is_editable, True)
#         self.assertEqual(v.get_info(), None)

#     @patch('package_monitor.models.package_info', mock_info)
#     def test_update_from_pypi(self):
#         """Test the update_from_pypi method."""
#         # editable packages return None
#         r = requirement.Requirement.parse("foobar==0.0.1")
#         v = models.PackageVersion(requirement=r)
#         v.update_from_pypi()
#         self.assertEqual(v.licence, TEST_INFO.get('license'))
#         self.assertEqual(v.current_version, Version('0.0.1'))
#         self.assertEqual(v.latest_version, Version(TEST_INFO['version']))
#         self.assertEqual(v.diff_status, 'major')
