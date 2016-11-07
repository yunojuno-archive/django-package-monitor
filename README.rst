.. image:: https://travis-ci.org/yunojuno/django-package-monitor.svg?branch=master
    :target: https://travis-ci.org/yunojuno/django-package-monitor

.. image:: https://badge.fury.io/py/django-package-monitor.svg
    :target: https://badge.fury.io/py/django-package-monitor

.. image:: https://codecov.io/gh/yunojuno/django-package-monitor/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/yunojuno/django-package-monitor


Django Package Monitor
======================

A Django app for keeping track of dependency updates.

Background
----------

At YunoJuno we have a Django project that includes almost 100 external packages.
In order to manage updates to these we have a rolling development task that
comes around in the first week of each month, and includes the following:

1. Using ``pip list --outdated`` list out all available updates
2. Group updates (using `semver <http://semver.org/>`_) into Major, Minor, Patch, Other
3. Apply patch updates in a single update / commit
4. Apply minor updates as a group, see what breaks, remove, rinse, repeat
5. Take a view on major updates

This task is a PITA, and so we decided to make it simpler.

Implementation
--------------

This project contains a Django app that can be used to monitor your packages.

It consists of a single model, ``PackageVersion``, an admin list view that you
can use to view current package versions, and load latest versions from PyPI,
and a single management command that can be used to load local requirements and
update remote versions from the shell - which you could run overnight if you
felt the need.

It is important to note that this app **does not** update your requirements for
you - it simply displays the requirements that you have, and the latest that
is available on PyPI.

In order to illustrate how it works, the app itself contains a Django project
that can be used to demonstrate the feature.

Installation
------------

Download / install the app using pip:

.. code:: shell

    pip install django-package-monitor

Add the app ``package_monitor`` to your ``INSTALLED_APPS`` Django setting:

.. code:: python

    # settings.py
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'package_monitor',
        ...
    )

Set the ``PACKAGE_MONITOR_REQUIREMENTS_FILE`` setting to point to your project
requirements file:

.. code:: python

   # settings.py
   PACKAGE_MONITOR_REQUIREMENTS_FILE = path.join(PROJECT_ROOT, 'requirements.txt')


Add the app URLs to your project - NB it must have the namespace set:

.. code:: python

    # urls.py
    urlpatterns = patterns(
        '',
        url(r'^admin/', include(admin.site.urls)),
        url(r'^package_monitor/', include('package_monitor.urls', namespace='package_monitor')),
    )

At this point you should have a working implementation. You can test this by running
the management command to load your local requirements:

.. code:: shell

    # load up the local requirements file
    $ python manage.py refresh_packages --local

This will load all of the requirements it finds in the requirements file specified into the
database. If you then want to check PyPI for updated version, run the command with the ``--remote``
option. You can run both of these command together:

.. code:: python

    # load up the local requirements file, and check PyPI
    $ python manage.py refresh_packages --local --remote

If you want to clean out the existing ``PackageVersion`` table before loading the local file, use the ``--clean``
option:

.. code:: shell

    # clear out database, load up the local requirements file, and check PyPI
    $ python manage.py refresh_packages --clean --local --remote

Tests
-----

There is a test suite that can be run using tox:

.. code:: shell

    $ pip install -r requirements
    $ tox

In addition to the unit tests, the source distribution also includes a fully-functioning Django
project, that can be run from the repo root, and used to demonstrate how it works:

.. code:: shell

    $ git clone git@github.com:yunojuno/django-package-monitor.git
    $ cd django-package-monitor
    $ pip install -r requirements.txt
    # you will need to create a superuser in order to access the admin site
    $ python manage.py createsuperuser
    $ python manage.py runserver

If you then log in to the app (http://localhost:8000/admin by default), you can then see the admin
list page:

.. image:: https://github.com/yunojuno/django-package-monitor/blob/master/screenshots/no_packages.png
   :alt: Screenshot of admin list view (empty)

If you click on the "Reload local requirements" button in the top-right, it will load up the contents
of the requirements file that you used earlier:

.. image:: https://github.com/yunojuno/django-package-monitor/blob/master/screenshots/local_only.png
   :alt: Screenshot of admin list view populated with local requirements

NB If any requirements cannot be parsed by the ``semantic_version.Version.coerce`` method, then the
``is_parseable`` property is set to `False`, and the package is in effect unmanaged.

At this point it has parsed the requirements file, and stored the current working version of
each package (as ``current_version``). In order to see what the latest versions are, select all the packages,
and choose "Update selected packages from PyPI" form the actions list:

.. image:: https://github.com/yunojuno/django-package-monitor/blob/master/screenshots/select_all.png
   :alt: Screenshot of admin list view with all requirements selected

This may take some time, as it will call the PyPI API for each package (excluding those that are
marked as editable), and download the latest version info for each. At the end of this, you should
see the page updated with the new version information (as ``latest_version``) - as well as the licence
information that is stored in the PyPI metadata:

.. image:: https://github.com/yunojuno/django-package-monitor/blob/master/screenshots/remote.png
   :alt: Screenshot of admin list view with requirement info updated from PyPI

If you drill down to the detail on an individual package, you can see all of the available versions:

.. image:: https://github.com/yunojuno/django-package-monitor/blob/master/screenshots/package_details.png
   :alt: Screenshot of Django package details

Contributing
------------

This is by no means complete - it can't cope with requirements that are anything other than '==',
and it doesn't (yet) help with updating the requirements file itself. However, it's good enough to
be of value, hence releasing it. If you would like to contribute to the project, usual Github rules
apply:

1. Fork the repo to your own account
2. Submit a pull request
3. Add tests for any new code
4. Follow coding style of existing project

Licence
-------

This project is MIT licensed - see the LICENCE file for details.
