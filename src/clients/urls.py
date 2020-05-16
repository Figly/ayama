from django.urls import path
from .forms import AddClientDetailForm, AddClientContactDetailForm, AddClientEmploymentetailForm, AddClientRatesAndReturnForm, AddClientDependentDetailsForm
from .views import ClientWizard
from . import views

app_name = "clients"
urlpatterns = [
    path("clients/", ClientWizard.as_view([AddClientDetailForm, AddClientContactDetailForm, AddClientEmploymentetailForm, AddClientRatesAndReturnForm]), name="add-client"),
    path("add_client_dependents/", views.AddClientDependentView.as_view(), name="add-client-dependents")
]
