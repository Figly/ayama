from django.urls import path

from .forms import (AddClientContactDetailForm, AddClientDependentDetailsForm,
                    AddClientDetailForm, AddClientEmploymentetailForm,
                    AddClientRatesAndReturnForm)
from .views import (AddClientDependentView, ClientlistView, ClientSummaryView,
                    ClientWizard)

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
        AddClientDependentView.as_view(),
        name="add-client-dependents",
    ),
    path('clients_list/', ClientlistView.as_view(), name='clients-list'),
    path(
        "client_summary/<pk>/",
        ClientSummaryView.as_view(), name='client-summary'
    ),
]
