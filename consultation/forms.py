from django import forms
from .models import *

class ComposeForm(forms.Form):
    message = forms.CharField(
            widget=forms.TextInput(
                attrs={"class": "form-control"}
                )
            )

class GoogleFitDataForm(forms.ModelForm):
    class Meta:
        model = GoogleFitVisualisation
        fields = ['health_data_file','health_data_url']
