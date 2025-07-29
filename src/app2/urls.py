from django.urls import path
from .views.product_info import product_info
from .views.product_search import product_search


urlpatterns = [
    path("product_search/", product_search, name="product_search"),
    path("product/<signed_value>/", product_info, name="product_info"),
]