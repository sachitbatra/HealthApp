from django.contrib import admin
from django.urls import path, re_path

from .views import *

app_name = 'consultation'
urlpatterns = [
    path(r'select_doctor', select_doctor, name='select_doctor'),
    path(r'google_fit', google_fit, name='google_fit'),
    path(r'google_fit_data_visualisation', google_fit_data_visualisation, name='google_fit_data_visualisation'),
    path('', InboxView.as_view()),
    re_path(r"^(?P<username>[\w.@+-]+)", ThreadView.as_view())
]
