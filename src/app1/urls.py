from django.urls import path
from .views.home import home
from .views.add_deal import add_deal
from .views.last_deals import last_deals


urlpatterns = [
    path("", home, name="home"),
    path("last_deals/", last_deals, name="last_deals"),
    path("add_deal/", add_deal, name="add_deal"),
]