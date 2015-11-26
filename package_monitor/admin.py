# -*- coding: utf8 -*-
import json
import logging

from django.http import HttpResponseRedirect
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.template.defaultfilters import truncatechars

from package_monitor.models import PackageVersion

logger = logging.getLogger(__name__)


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
        'package_name', 'is_editable', 'current_version',
        'latest_version', '_licence', 'diff_status', 'checked_pypi_at'
    )
    list_filter = ('diff_status',)
    ordering = ["package_name"]
    readonly_fields = (
        'package_name', 'is_editable', 'current_version',
        'latest_version', 'diff_status', 'checked_pypi_at',
        'url', 'licence', 'raw'
    )

    def _licence(self, obj):
        """Return truncated version of licence."""
        return truncatechars(obj.licence, 20)
    _licence.short_description = "PyPI licence"

admin.site.register(PackageVersion, PackageVersionAdmin)
