from django.conf.urls import url
from django.urls import path
from . import views
app_name = 'doctor_core'
urlpatterns = [
    path('signed_in/',views.signed_in),
    path('view_profile/',views.view_profile,name='view_profile'),
    path('create_profile/',views.create_profile,name='create_profile'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('ongoing_consultations/',views.view_ongoing_consultations,name='ongoing_consultations'),
    path('previous_consultations/',views.view_past_consultations,name='previous_consultations'),
    path('feedback/',views.view_feedback,name='feedback'),
]