from django.urls import path
from .forms import AddClientDetailForm, AddClientContactDetailForm, AddClientEmploymentetailForm, AddClientRatesAndReturnForm, AddClientDependentDetailsForm
from .views import ClientWizard

app_name = "clients"
urlpatterns = [
    path("clients/", ClientWizard.as_view([AddClientDetailForm, AddClientContactDetailForm, AddClientEmploymentetailForm, AddClientRatesAndReturnForm, AddClientDependentDetailsForm]), name="add-client"),
]
