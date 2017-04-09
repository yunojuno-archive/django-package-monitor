# -*- coding: utf-8 -*-
"""Python 2/3 compatibility imports."""
try:
    from unittest import mock
    print("Successfully imports mock from unittest")
except ImportError:
    print("Trying to import standalone mock")
    import mock  # noqa
    print("Successfully imported standalone mock")
