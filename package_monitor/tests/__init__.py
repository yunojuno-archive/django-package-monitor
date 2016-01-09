# -*- coding: utf-8 -*-
import json
from os import path


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
