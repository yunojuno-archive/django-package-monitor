"""Management command for syncing requirements."""
from argparse import ArgumentParser
from collections import defaultdict
from logging import getLogger
from typing import Any, Dict, List

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.template.loader import render_to_string
from django.utils.timezone import now as tz_now
from requirements.parser import parse
from requirements.requirement import Requirement

from ...models import PackageVersion
from ...settings import REQUIREMENTS_FILE

logger = getLogger(__name__)


def create_package_version(requirement: Requirement) -> None:
    """Create a new PackageVersion from a requirement. Handles errors."""
    try:
        PackageVersion(requirement=requirement).save()
        logger.info("Package '%s' added.", requirement.name)  # noqa
    except IntegrityError:
        logger.info("Package '%s' already exists.", requirement.name)  # noqa


def local() -> None:
    """Load local requirements file."""
    logger.info("Loading requirements from local file.")
    with open(REQUIREMENTS_FILE, "r") as f:
        requirements = parse(f)
        for r in requirements:
            logger.debug("Creating new package: %r", r)
            create_package_version(r)


def remote() -> Dict[str, List]:
    """Update package info from PyPI."""
    logger.info("Fetching latest data from PyPI.")
    results = defaultdict(list)
    packages = PackageVersion.objects.exclude(is_editable=True)
    for pv in packages:
        pv.update_from_pypi()
        results[pv.diff_status].append(pv)
        logger.debug("Updated package from PyPI: %r", pv)
    results["refreshed_at"] = tz_now()
    return results


def clean() -> None:
    """Clean out all packages."""
    PackageVersion.objects.all().delete()
    logger.info("Deleted all existing packages.")


class Command(BaseCommand):

    help = (
        "This command can be used to load up a requirements file "
        "and check against PyPI for updates."
    )

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--local",
            action="store_true",
            dest="local",
            default=False,
            help="Load local requirements file",
        )
        parser.add_argument(
            "--remote",
            action="store_true",
            dest="remote",
            default=False,
            help="Load latest from PyPI",
        )
        parser.add_argument(
            "--clean",
            action="store_true",
            dest="clean",
            default=False,
            help="Delete all existing requirements",
        )
        parser.add_argument("--notify", help="Send results notification email")
        parser.add_argument(
            "--from",
            default="Django Package Monitor <packages@example.com>",
            help="Notification email 'from' address",
        )
        parser.add_argument(
            "--subject",
            default="Package manager update",
            help="Notification email subject line.",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Run the managemement command."""
        if options["clean"]:
            clean()

        if options["local"]:
            local()

        if options["remote"]:
            results = remote()
            if options["notify"]:
                send_mail(
                    options["subject"],
                    render_to_string("summary.txt", results),
                    options["from"],
                    [options["notify"]],
                    html_message=render_to_string("summary.html", results),
                    fail_silently=False,
                )
