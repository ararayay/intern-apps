from django.urls import path
from .views.employees import employees


urlpatterns = [
    path("", employees, name="employees"),
]