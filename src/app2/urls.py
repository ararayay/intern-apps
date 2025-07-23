from django.urls import path
from . import views


urlpatterns = [
    path("product_search/", views.product_search, name="product_search"),
    path("product/<signed_value>/", views.product_info, name="product_info"),
]