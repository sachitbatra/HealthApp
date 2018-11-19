from django.contrib import admin
from django.urls import path, re_path

from .views import *

app_name = 'consultation'
urlpatterns = [
    path(r'select_doctor', select_doctor, name='select_doctor'),
    path('', InboxView.as_view()),
    path('ongoing_consultations',ongoing_consultations,name='ongoing_consultations'),
    path('past_consultations',past_consultations,name='past_consultations'),
    re_path(r"^(?P<username>[\w.@+-]+)", ThreadView.as_view())
]
