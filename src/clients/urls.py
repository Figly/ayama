from django.urls import path

from . import views

app_name = "clients"
urlpatterns = [
    path("add_client/", views.AddClientDetailView.as_view(), name="add-client"),
    path("add_client_contact/<int:cid>", views.AddClientContactDetailView.as_view(), name="add-client-contact"),
    path("add_client_employement/<int:cid>", views.AddClientEmploymentDetailView.as_view(), name="add-client-employment"),
    path("add_client_rates/<int:cid>", views.AddClientRatesView.as_view(), name="add-client-rates"),
    path("add_client_dependent/<int:cid>", views.AddClientDependentDetailView.as_view(), name="add-client-dependent"),
]
