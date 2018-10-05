from django import forms
from .models import UserModel


class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['name', 'email_address', 'password', 'age']


class LogInForm(forms.Form):
    email_address = forms.EmailField()
    password = forms.CharField(max_length=4096)
