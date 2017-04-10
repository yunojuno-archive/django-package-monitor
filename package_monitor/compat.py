# -*- coding: utf-8 -*-
"""Python 2/3 compatibility imports."""
try:
    from unittest import mock
except ImportError:
    import mock  # noqa
