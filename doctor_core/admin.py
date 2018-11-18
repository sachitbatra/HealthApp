from django.contrib import admin

# Register your models here.
from .models import DoctorProfile,Consultation,FeedBack

admin.site.register(DoctorProfile)
admin.site.register(Consultation)
admin.site.register(FeedBack)