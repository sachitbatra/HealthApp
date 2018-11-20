from django.conf.urls import url
from django.urls import path
from . import views
app_name = 'user_core'

urlpatterns = [
    path('signed_in/',views.signed_in,name='signed_in'),
    path('search/',views.search_doctor,name='search'),
    path('go_to_chat/',views.go_to_chat,name='go_to_chat'),
]