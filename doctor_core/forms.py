from django import forms
from .models import DoctorProfile

class CreateProfile(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['bio','phone_no','image']
