from django.urls import path

from .forms import (
    AddAdministratorContactDetailForm,
    AddAdministratorDetailForm,
    AddAdvisorContactDetailForm,
    AddAdvisorDetailForm,
    AddPractiseDetailForm,
    SignUpAdministratorDetailForm,
)
from .views import (
    AddPractiseView,
    AdministratorSummaryView,
    AddAdministratorWizard,
    AdvisorlistView,
    AdvisorSummaryView,
    AdvisorWizard,
    AministratorlistView,
    EditAdministratorContactView,
    EditAdministratorDetailView,
    EditAdvisorContactView,
    EditAdvisorDetailView,
    EditPractiseView,
    EditReminderPreferencesView,
    SignUpAdministratorWizard,
)

app_name = "practises"
urlpatterns = [
    path("add_practise/", AddPractiseView.as_view(), name="add-practise"),
    path("edit_practise/<pk>/", EditPractiseView.as_view(), name="edit-practise"),
    path(
        "advisor/",
        AdvisorWizard.as_view([AddAdvisorDetailForm, AddAdvisorContactDetailForm]),
        name="add-advisor",
    ),
    path(
        "advisor/<int:practise>/",
        AdvisorWizard.as_view([AddAdvisorDetailForm, AddAdvisorContactDetailForm]),
        name="add-advisor",
    ),
    path(
        "administrator/",
        AddAdministratorWizard.as_view(
            [AddAdministratorDetailForm, AddAdministratorContactDetailForm]
        ),
        name="add-administrator",
    ),
    path(
        "admin_sign_up/",
        SignUpAdministratorWizard.as_view(
            [
                SignUpAdministratorDetailForm,
                AddAdministratorContactDetailForm,
                AddPractiseDetailForm,
            ]
        ),
        name="sign-up-administrator",
    ),
    path("advisor_list/", AdvisorlistView.as_view(), name="advisor-list"),
    path("advisor_summary/<pk>/", AdvisorSummaryView.as_view(), name="advisor-summary"),
    path(
        "edit_advisor_detail/<pk>/",
        EditAdvisorDetailView.as_view(),
        name="edit-advisor-detail",
    ),
    path(
        "edit_advisor_contact/<pk>/",
        EditAdvisorContactView.as_view(),
        name="edit-advisor-contact",
    ),
    path(
        "administrator_list/", AministratorlistView.as_view(), name="administrator-list"
    ),
    path(
        "administrator_summary/<pk>/",
        AdministratorSummaryView.as_view(),
        name="administrator-summary",
    ),
    path(
        "edit_administrator_detail/<pk>/",
        EditAdministratorDetailView.as_view(),
        name="edit-administrator-detail",
    ),
    path(
        "edit_administrator_contact/<pk>/",
        EditAdministratorContactView.as_view(),
        name="edit-administrator-contact",
    ),
    path(
        "edit_advisor_reminder/<pk>/",
        EditReminderPreferencesView.as_view(),
        name="edit-advisor-reminder-config",
    ),
]
