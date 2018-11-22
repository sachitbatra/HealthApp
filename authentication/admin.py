from django.contrib import admin

# Register your models here.
from .models import UserModel, DoctorModel

admin.site.register(UserModel)
admin.site.register(DoctorModel)