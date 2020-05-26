from django.urls import path

from . import views
from .forms import (
    AddClientContactDetailForm,
    AddClientDependentDetailsForm,
    AddClientDetailForm,
    AddClientEmploymentetailForm,
    AddClientRatesAndReturnForm,
)
from .views import ClientWizard

app_name = "clients"
urlpatterns = [
    path(
        "clients/",
        ClientWizard.as_view(
            [
                AddClientDetailForm,
                AddClientContactDetailForm,
                AddClientEmploymentetailForm,
                AddClientRatesAndReturnForm,
            ]
        ),
        name="add-client",
    ),
    path(
        "add_client_dependents/",
        views.AddClientDependentView.as_view(),
        name="add-client-dependents",
    ),
]
