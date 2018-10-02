from django import forms
from .models import UserModel


class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['name', 'email_address', 'password', 'age']
