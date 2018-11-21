from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *

class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routines
        fields = ['exc','reps','sets']
        labels = {
            "exc":"Exercise",
            "reps":"Repetitions",
            "sets":"Sets"
        }

# class ExerciseForm(forms.ModelForm):
#     class Meta:
#         model = Exercise
#         fields = ['rtn']
class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['name','starttime','endtime']
        labels = {
            "starttime":"From",
            "endtime":"To"
        }
