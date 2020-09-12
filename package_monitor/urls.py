from django.urls import path

from . import views

app_name = "package_monitor"

urlpatterns = [path("reload/", views.reload, name="reload")]
