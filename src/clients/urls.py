from django.urls import path

from .forms import (
    AddClientContactDetailForm,
    AddClientDependentDetailsForm,
    AddClientDetailForm,
    AddClientEmploymentDetailForm,
    AddClientNoteForm,
    AddClientRatesAndReturnForm,
)
from .views import (
    AddClientDependentView,
    AddClientNoteView,
    AdvisorClientsView,
    ClientlistView,
    ClientNoteListView,
    ClientSummaryView,
    ClientWizard,
    EditClientCommunicationFrequencyView,
    EditClientContactView,
    EditClientDependentView,
    EditClientDetailsView,
    EditClientEmploymentView,
    EditClientNoteView,
    EditClientRatesView,
    UpdateClientCommunicationHistoryView,
)

app_name = "clients"
urlpatterns = [
    path(
        "clients/",
        ClientWizard.as_view(
            [
                AddClientDetailForm,
                AddClientContactDetailForm,
                AddClientEmploymentDetailForm,
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
    path("clients_list/", ClientlistView.as_view(), name="clients-list"),
    path("advisor_clients/", AdvisorClientsView.as_view(), name="advisor-clients"),
    path("client_summary/<pk>/", ClientSummaryView.as_view(), name="client-summary"),
    path(
        "edit_client/<pk>/", EditClientDetailsView.as_view(), name="edit-client-details"
    ),
    path(
        "edit_client_contact/<pk>/",
        EditClientContactView.as_view(),
        name="edit-client-contact",
    ),
    path(
        "edit_client_employment/<pk>/",
        EditClientEmploymentView.as_view(),
        name="edit-client-employment",
    ),
    path(
        "edit_client_rates/<pk>/",
        EditClientRatesView.as_view(),
        name="edit-client-rates",
    ),
    path(
        "edit_client_dependent/<pk>/",
        EditClientDependentView.as_view(),
        name="edit-client-dependent",
    ),
    path(
        "edit_client_communication_frequency/<pk>/",
        EditClientCommunicationFrequencyView.as_view(),
        name="edit-client-communication-frequency",
    ),
    path("add_client_note/", AddClientNoteView.as_view(), name="add-client-note",),
    path(
        "edit_client_note/<pk>/", EditClientNoteView.as_view(), name="edit-client-note",
    ),
    path(
        "client_note_list/<pk>/", ClientNoteListView.as_view(), name="client-note-list",
    ),
    path(
        "client_comms_hist/<pk>/",
        UpdateClientCommunicationHistoryView.as_view(),
        name="edit-client-comms",
    ),
]
