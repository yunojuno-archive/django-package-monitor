# -*- coding=utf-8 -*-
from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    'package_monitor.views',
    url(r'^reload/', 'reload', name='reload')
)
