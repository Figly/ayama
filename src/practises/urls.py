from django.urls import path

from .forms import (
    AddAdministratorContactDetailForm,
    AddAdministratorDetailForm,
    AddAdvisorContactDetailForm,
    AddAdvisorDetailForm,
)
from .views import (
    AddPractiseView,
    AdministratorWizard,
    AdvisorlistView,
    AdvisorSummaryView,
    AdvisorWizard,
)

app_name = "practises"
urlpatterns = [
    path("add_practise/", AddPractiseView.as_view(), name="add-practise"),
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
]
