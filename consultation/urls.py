from django.contrib import admin
from django.urls import path, re_path

from .views import *

app_name = 'consultation'
urlpatterns = [
    path('', InboxView.as_view()),
    re_path(r"^(?P<username>[\w.@+-]+)", ThreadView.as_view())
]