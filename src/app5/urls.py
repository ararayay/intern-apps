from django.urls import path
from .views.add_contacts import add_contacts
from .views.export_contacts import export_contacts


urlpatterns = [
    path("add/", add_contacts, name="add_contacts"),
    path("export/", export_contacts, name="export_contacts"),
]