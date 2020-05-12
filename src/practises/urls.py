from django.urls import path

from . import views

app_name = "practises"
urlpatterns = [
    path("add_practise/", views.AddPractiseView.as_view(), name="add-practise"),
    path("add_advisor/", views.AddAdvisorDetailView.as_view(), name="add-advisor"),
    path("add_advisor_contact/", views.AddAdvisorContactDetailView.as_view(), name="add-advisor-contact"),
    path("add_administrator/", views.AddAdministratorView.as_view(), name="add-administrator"),
    path("add_administrator_contact/", views.AddAdministratorContactDetailView.as_view(), name="add-administrator-contact"),
]
