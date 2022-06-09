from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.data_from_csv, name="index"),
]
