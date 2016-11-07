# *-8 coding: utf-8 -*-
"""Parse requirements file, and work out whether there are any updates."""
import logging

from django.db import models
from django.utils.timezone import now as tz_now

from semantic_version import Version
from semantic_version.django_fields import VersionField

from . import pypi


logger = logging.getLogger(__name__)


class PackageVersion(models.Model):

    """A specific version of a package."""

    DIFF_CHOICES = (
        ('unknown', 'Unknown'),
        ('none', 'Up-to-date'),
        ('major', 'Major'),
        ('minor', 'Minor'),
        ('patch', 'Patch'),
        ('other', 'Other'),
    )

    raw = models.CharField(
        max_length=200,
        help_text="The line specified in the requirements file."
    )
    package_name = models.CharField(
        unique=True,
        max_length=100,
        help_text="The name of the package on PyPI."
    )
    current_version = VersionField(
        null=True, blank=True,
        help_text="The current version as specified in the requirements file. "
    )
    latest_version = VersionField(
        null=True, blank=True,
        help_text="Latest version available from PyPI."
    )
    next_version = VersionField(
        null=True, blank=True,
        help_text="Next available version available from PyPI."
    )
    licence = models.CharField(
        max_length=100,
        blank=True,
        help_text="The licence used (extracted from PyPI info)."
    )
    diff_status = models.CharField(
        max_length=10,
        choices=DIFF_CHOICES,
        default='unknown',
        help_text=(
            "The diff between current and latest versions. "
            "Updated via update_latest_version."
        )
    )
    checked_pypi_at = models.DateTimeField(
        null=True, blank=True,
        help_text="When PyPI was last checked for this package."
    )
    is_editable = models.BooleanField(
        "Editable (-e)",
        default=False,
        help_text="True if this requirement is specified with '-e' flag."
    )
    is_parseable = models.BooleanField(
        "Parseable",
        default=False,
        help_text="True if the version can be parsed as a valid semver version."
    )
    url = models.URLField(
        null=True, blank=True,
        help_text="The PyPI URL to check - (blank if editable)."
    )

    class Meta:
        ordering = ["package_name"]
        verbose_name_plural = "Package versions"

    def __init__(self, *args, **kwargs):
        requirement = kwargs.pop('requirement', None)
        super(PackageVersion, self).__init__(*args, **kwargs)
        if requirement is None:
            return
        self.raw = requirement.line
        self.package_name = requirement.name
        self.is_editable = requirement.editable
        if requirement.editable:
            self.url = ''
            self.current_version = None
        else:
            # HACK: we only take the first version.
            try:
                self.current_version = Version.coerce(requirement.specs[0][1])
                self.is_parseable = True
            except ValueError as ex:
                self.current_version = None
                self.is_parseable = False
                logger.debug("Unparseable package version (%s): %s", requirement.specs[0][1], ex)
            self.url = pypi.package_url(requirement.name)

    def __unicode__(self):
        return u"Package '%s'" % self.raw

    def __str__(self):
        return unicode(self).encode('utf-8')

    def update_from_pypi(self):
        """Call get_latest_version and then save the object."""
        package = pypi.Package(self.package_name)
        self.licence = package.licence()
        if self.is_parseable:
            self.latest_version = package.latest_version()
            self.next_version = package.next_version(self.current_version)
            self.diff_status = pypi.version_diff(self.current_version, self.latest_version)
        self.checked_pypi_at = tz_now()
        self.save()
        return self
