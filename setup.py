from os import chdir, pardir, path

from setuptools import find_packages, setup

README = open(path.join(path.dirname(__file__), "README.rst")).read()

# allow setup.py to be run from any path
chdir(path.normpath(path.join(path.abspath(__file__), pardir)))

setup(
    name="django-package-monitor",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "django>=2.0",
        "requests",
        "requirements_parser",
        "semantic_version",
    ],
    include_package_data=True,
    description="Requirements package monitor for Django projects.",
    license="MIT",
    long_description=README,
    url="https://github.com/yunojuno/django-package-monitor",
    author="YunoJuno",
    author_email="code@yunojuno.com",
    maintainer="YunoJuno",
    maintainer_email="cod@yunojuno.com",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
