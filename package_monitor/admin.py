# -*- coding: utf8 -*-
import logging

from django.contrib import admin
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe

from package_monitor.models import PackageVersion

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


class PackageVersionAdmin(admin.ModelAdmin):

    actions = (check_pypi,)
    change_list_template = 'change_list.html'
    list_display = (
        'package_name', 'is_editable', '_updateable', 'current_version', 'next_version',
        'latest_version', '_licence', 'diff_status', 'checked_pypi_at'
    )
    list_filter = ('diff_status', 'is_editable')
    ordering = ["package_name"]
    readonly_fields = (
        'package_name', 'is_editable', 'current_version', 'next_version',
        'latest_version', 'diff_status', 'checked_pypi_at',
        'url', 'licence', 'raw', 'available_updates'
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
