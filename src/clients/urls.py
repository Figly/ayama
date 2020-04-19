from django.urls import path

from . import views

app_name = "clients"
urlpatterns = [
    path("add_client/", views.AddClientDetailView.as_view(), name="add-client"),
    path("add_client_contact/", views.AddClientContactDetailView.as_view(), name="add-client-contact"),
]
