from django.conf.urls import url
from django.urls import path
from . import views
app_name = 'doctor_core'
urlpatterns = [
    path('signed_in/',views.signed_in),
    path('view_profile/',views.view_profile,name='view_profile'),
    path('create_profile/',views.create_profile,name='create_profile'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
]