# -*- coding=utf-8 -*-
from django.conf.urls import url

from .views import reload

urlpatterns = [
    url(r'^reload/', reload, name='reload')
]
