from django import forms
from .models import DoctorProfile,FeedBack,Consultation

class CreateProfile(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['bio','phone_no','image']
class CreateFeedBack(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ['feedback','overall_rating','quickness','treatment']
class CreatePostConsultation(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['diagnosis','notes']
    #consultation_id = forms.IntegerField()