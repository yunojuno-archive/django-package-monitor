# *-8 coding: utf-8 -*-
"""Parse requirements file, and work out whether there are any updates."""
import logging

from django.db import models
from django.utils.timezone import now as tz_now

from semantic_version import Version
from semantic_version.django_fields import VersionField

from package_monitor import (
    package_url,
    package_info,
    package_version,
    package_licence,
    version_diff
)

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
        default=False,
        help_text="True if this requirement is specified with '-e' flag."
    )
    url = models.URLField(
        null=True, blank=True,
        help_text="The URL to check - PyPI or repo (if editable)."
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
            self.url = requirement.uri
        else:
            # HACK: we only take the first version.
            self.current_version = Version.coerce(requirement.specs[0][1])
            self.url = package_url(requirement.name)

    def __unicode__(self):
        return u"Package '%s'" % self.raw

    def __str__(self):
        return unicode(self).encode('utf-8')

    def get_info(self):
        """Check PyPI for the latest version of the package.

        Returns the 'info' block of the PyPI JSON as JSON. This contains
        all the information that PyPI has on the release.

        """
        return None if self.is_editable else package_info(self.url)

    def update_from_pypi(self):
        """Call get_latest_version and then save the object."""
        info  = self.get_info()
        self.licence = package_licence(info)
        self.latest_version = package_version(info)
        self.diff_status = version_diff(self.current_version, self.latest_version)
        self.checked_pypi_at = tz_now()
        self.save()
        return self
