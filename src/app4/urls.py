from django.urls import path
from .views.companies_map import companies_map


urlpatterns = [
    path("", companies_map, name="companies_map"),
]