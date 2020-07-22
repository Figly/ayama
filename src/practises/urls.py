from django.urls import path

from .forms import (
    AddAdministratorContactDetailForm,
    AddAdministratorDetailForm,
    AddAdvisorContactDetailForm,
    AddAdvisorDetailForm,
    AddPractiseDetailForm,
    SignUpAdministratorDetailForm,
    SignUpAdvisorDetailForm,
)
from .views import (
    AddAdministratorWizard,
    AddAdvisorWizard,
    AddPractiseView,
    AddProductView,
    AdministratorlistView,
    AdministratorSummaryView,
    AdvisorlistView,
    AdvisorSummaryView,
    EditAdministratorContactView,
    EditAdministratorDetailView,
    EditAdvisorContactView,
    EditAdvisorDetailView,
    EditPractiseView,
    EditProductView,
    EditReminderPreferencesView,
    EditRolesView,
    LinkClientProductView,
    ProductlistView,
    SignUpAdministratorWizard,
    SignUpAdvisorWizard,
)

app_name = "practises"
urlpatterns = [
    path("add_practise/", AddPractiseView.as_view(), name="add-practise"),
    path("edit_practise/<pk>/", EditPractiseView.as_view(), name="edit-practise"),
    path(
        "advisor/",
        AddAdvisorWizard.as_view([AddAdvisorDetailForm, AddAdvisorContactDetailForm]),
        name="add-advisor",
    ),
    path(
        "advisor/<int:practise>/",
        AddAdvisorWizard.as_view([AddAdvisorDetailForm, AddAdvisorContactDetailForm]),
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
    path(
        "advisor_sign_up/",
        SignUpAdvisorWizard.as_view(
            [SignUpAdministratorDetailForm, AddAdvisorContactDetailForm]
        ),
        name="sign-up-advisor",
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
        "administrator_list/",
        AdministratorlistView.as_view(),
        name="administrator-list",
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
    path(
        "edit_advisor_roles/<pk>/", EditRolesView.as_view(), name="edit-advisor-roles",
    ),
    path("add_product/", AddProductView.as_view(), name="add-product"),
    path("product_list/", ProductlistView.as_view(), name="list-products"),
    path("edit_product/<pk>/", EditProductView.as_view(), name="edit-product"),
    path(
        "link_client_product/<int:client_id>",
        LinkClientProductView.as_view(),
        name="link-client-product",
    ),
]
