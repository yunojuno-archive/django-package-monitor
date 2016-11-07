# -*- coding: utf8 -*-
import logging

from django.contrib import admin
from django.db.models import F
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe

from .models import PackageVersion

logger = logging.getLogger(__name__)


def html_list(data):
    """Convert dict into formatted HTML."""
    if data is None:
        return None
    as_li = lambda v: "<li>%s</li>" % v
    items = [as_li(v) for v in data]
    return mark_safe("<ul>%s</ul>" % ''.join(items))


def check_pypi(modeladmin, request, queryset):
    """Update latest package info from PyPI."""
    for p in queryset:
        if p.is_editable:
            logger.debug("Ignoring version update '%s' is editable", p.package_name)
        else:
            p.update_from_pypi()
check_pypi.short_description = "Update selected packages from PyPI"


class UpdateAvailableListFilter(admin.SimpleListFilter):

    """Enable filtering by packages with an update available."""

    title = "Update available"
    parameter_name = 'update'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Yes'),
            ('0', 'No'),
            ('-1', 'Unknown'),
        )

    def queryset(self, request, queryset):
        """Filter based on whether an update (of any sort) is available."""
        if self.value() == '-1':
            return queryset.filter(latest_version__isnull=True)
        elif self.value() == '0':
            return (
                queryset
                .filter(
                    current_version__isnull=False,
                    latest_version__isnull=False,
                    latest_version=F('current_version')
                )
            )
        elif self.value() == '1':
            return (
                queryset
                .filter(
                    current_version__isnull=False,
                    latest_version__isnull=False
                ).exclude(
                    latest_version=F('current_version')
                )
            )
        else:
            return queryset


class PackageVersionAdmin(admin.ModelAdmin):

    actions = (check_pypi,)
    change_list_template = 'change_list.html'
    list_display = (
        'package_name', 'is_editable', '_updateable', 'current_version', 'next_version',
        'latest_version', '_licence', 'diff_status', 'checked_pypi_at', 'is_parseable'
    )
    list_filter = ('diff_status', 'is_editable', 'is_parseable', UpdateAvailableListFilter)
    ordering = ["package_name"]
    readonly_fields = (
        'package_name', 'is_editable', 'current_version', 'next_version',
        'latest_version', 'diff_status', 'checked_pypi_at',
        'url', 'licence', 'raw', 'available_updates', 'is_parseable'
    )

    def _licence(self, obj):
        """Return truncated version of licence."""
        return truncatechars(obj.licence, 20)
    _licence.short_description = "PyPI licence"

    def _updateable(self, obj):
        """Return True if there are available updates."""
        if obj.latest_version is None or obj.is_editable:
            return None
        else:
            return obj.latest_version != obj.current_version
    _updateable.boolean = True
    _updateable.short_description = u"Update available"

    def available_updates(self, obj):
        """Print out all versions ahead of the current one."""
        from package_monitor import pypi
        package = pypi.Package(obj.package_name)
        versions = package.all_versions()
        return html_list([v for v in versions if v > obj.current_version])

admin.site.register(PackageVersion, PackageVersionAdmin)
