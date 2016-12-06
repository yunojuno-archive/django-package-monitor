# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles import views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^package_monitor/', include('package_monitor.urls', namespace='package_monitor')),  # noqa
    url(r'^static/(?P<path>.*)$', views.serve),
]
