from django.urls import path

from . import views

app_name = "calculator"
urlpatterns = [
    path("main/", views.ShowCalcs.as_view(), name="show-calculator"),
]
