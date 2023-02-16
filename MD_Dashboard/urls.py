from django.urls import path, include
from . import views


urlpatterns = [
    path("choose", views.the_number_of_columns_choice, name="index"),
    path('one_column', views.one_column_view, name='one-column'),
    path('two_columns', views.data_from_csv, name='two-columns'),
    path("", views.upload_csv_view, name='upload')
]
