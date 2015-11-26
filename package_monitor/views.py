# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from package_monitor.management.commands import refresh_packages 


@user_passes_test(lambda u: u.is_staff)
def reload(request):
    """Reload local requirements file."""
    refresh_packages.clean()
    refresh_packages.local()
    url = request.META['HTTP_REFERER']
    return HttpResponseRedirect(url)