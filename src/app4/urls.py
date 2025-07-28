from django.urls import path
from . import views


urlpatterns = [
    path("", views.companies_map, name="companies_map"),
]