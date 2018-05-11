try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path

from . import views

app_name = 'package_monitor'

urlpatterns = [
    re_path(r'^reload/', views.reload, name='reload')
]
