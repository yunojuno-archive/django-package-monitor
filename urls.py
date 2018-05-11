from django.contrib import admin
from django.contrib.staticfiles import views
try:
    from django.urls import re_path, include
except ImportError:
    from django.conf.urls import url as re_path, include

admin.autodiscover()

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^package_monitor/', include('package_monitor.urls')),  # noqa
    re_path(r'^static/(?P<path>.*)$', views.serve),
]
