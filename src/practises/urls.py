from django.urls import path

from .forms import (AddAdministratorContactDetailForm,
                    AddAdministratorDetailForm, AddAdvisorContactDetailForm,
                    AddAdvisorDetailForm)
from .views import (AddPractiseView, AdministratorSummaryView,
                    AdministratorWizard, AdvisorlistView, AdvisorSummaryView,
                    AdvisorWizard, AministratorlistView,
                    EditAdministratorContactView, EditAdministratorDetailView,
                    EditAdvisorContactView, EditAdvisorDetailView,
                    EditPractiseView)

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
        AdministratorWizard.as_view(
            [AddAdministratorDetailForm, AddAdministratorContactDetailForm]
        ),
        name="add-administrator",
    ),
    path("advisor_list/", AdvisorlistView.as_view(), name="advisor-list"),
    path("advisor_summary/<pk>/", AdvisorSummaryView.as_view(), name="advisor-summary"),
    path("edit_advisor_detail/<pk>/", EditAdvisorDetailView.as_view(), name="edit-advisor-detail"),
    path("edit_advisor_contact/<pk>/", EditAdvisorContactView.as_view(), name="edit-advisor-contact"),
    path("administrator_list/", AministratorlistView.as_view(), name="administrator-list"),
    path("administrator_summary/<pk>/", AdministratorSummaryView.as_view(), name="administrator-summary"),
    path("edit_administrator_detail/<pk>/", EditAdministratorDetailView.as_view(), name="edit-administrator-detail"),
    path("edit_administrator_contact/<pk>/", EditAdministratorContactView.as_view(), name="edit-administrator-contact"),
]
