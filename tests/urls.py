from django.contrib import admin
from django.contrib.staticfiles import views
from django.urls import include, path

admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("package_monitor/", include("package_monitor.urls")),
    path("static/<str:path>", views.serve),
]
