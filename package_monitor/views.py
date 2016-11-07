# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect

from .management.commands import refresh_packages


@user_passes_test(lambda u: u.is_staff)
def reload(request):
    """Reload local requirements file."""
    refresh_packages.clean()
    refresh_packages.local()
    url = request.META.get('HTTP_REFERER')
    if url:
        return HttpResponseRedirect(url)
    else:
        return HttpResponse('Local requirements list has been reloaded.')
