# -*- coding: utf-8 -*-
"""Management command for syncing requirements."""
from logging import getLogger
from optparse import make_option

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from requirements import parse

from ...models import PackageVersion
from ...settings import REQUIREMENTS_FILE

logger = getLogger(__name__)


def create_package_version(requirement):
    """Create a new PackageVersion from a requirement. Handles errors."""
    try:
        PackageVersion(requirement=requirement).save()
        logger.info("Package '%s' added.", requirement.name)  # noqa
    except IntegrityError:
        logger.info("Package '%s' already exists.", requirement.name)  # noqa


def local():
    """Load local requirements file."""
    logger.info("Loading requirements from local file.")
    with open(REQUIREMENTS_FILE, 'r') as f:
        requirements = parse(f)
        for r in requirements:
            logger.debug("Creating new package: %r", r)
            create_package_version(r)


def remote():
    """Update package info from PyPI."""
    logger.info("Fetching latest data from PyPI.")
    for pv in PackageVersion.objects.exclude(is_editable=True):
        pv.update_from_pypi()
        logger.debug("Updated package from PyPI: %r", pv)


def clean():
    """Clean out all packages."""
    PackageVersion.objects.all().delete()
    logger.info("Deleted all existing packages.")


class Command(BaseCommand):

    help = (
        "This command can be used to load up a requirements file "
        "and check against PyPI for updates."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--local',
            action='store_true',
            dest='local',
            default=False,
            help='Load local requirements file'
        )
        parser.add_argument(
            '--remote',
            action='store_true',
            dest='remote',
            default=False,
            help='Load latest from PyPI'
        )
        parser.add_argument(
            '--clean',
            action='store_true',
            dest='clean',
            default=False,
            help='Delete all existing requirements'
        )

    def do_command(self, *args, **kwargs):
        raise NotImplementedError()

    def handle(self, *args, **options):
        """Run the managemement command."""

        if options['clean']:
            clean()

        if options['local']:
            local()

        if options['remote']:
            remote()
