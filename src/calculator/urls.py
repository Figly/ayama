from django.urls import path

from . import views

app_name = "calculator"
urlpatterns = [
    path("main/", views.ShowProfile.as_view(), name="show_self"),
]