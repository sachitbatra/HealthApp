from django.conf.urls import url
from django.urls import path
from .views import *
app_name = 'user_core'

urlpatterns = [
    path('signed_in/', signed_in, name='signed_in'),
    path('search/', search_doctor, name='search'),
    path('go_to_chat/', go_to_chat, name='go_to_chat'),
]