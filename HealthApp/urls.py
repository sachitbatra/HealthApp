"""HealthApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls import url,include
from django.conf.urls.static import static
from authentication.views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url('doc/signup', doc_signup_view,name='doc_signup'),
    url('doc/login', doc_login_view,name='doc_login'),
    #url('doc', doc_signup_view),
    url('^login', user_login_view,name='user_login'),
    url('^signup', user_signup_view,name='user_signup'),
    url('^logout', logout_view,name='logout'),
    url('^verification', verify_doctor),
    url('^error/', error_view),
    url(r'^api/user', UserOperations.as_view()),
    #url('', user_signup_view),  # Replace With HomePage
    url('doctor/',include("doctor_core.urls")),
    url('consultations/', include('consultation.urls')),
    path('admin/', admin.site.urls),
    url('user/',include("user_core.urls")),
]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

