from django.urls import path
from . import views

urlpatterns=[
    path('<int:schd_id>/rtn',views.routine_form,name="routine"),
    path('schedule',views.schedule_form,name="schedule"),
    path('view_schd',views.display_schedules.as_view(),name = "view_schd"),
    path('<int:schd_id>/view_rtns',views.display_routines.as_view(),name = "view_rtns"),
]
