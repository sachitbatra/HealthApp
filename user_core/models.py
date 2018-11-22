from django.db import models

# Create your models here.
from authentication.models import UserModel

class HealthProfile(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    height = models.FloatField()
    weight = models.FloatField()
    blood_grp = models.CharField(max_length=3)
    med_hist = models.TextField()
	#More need to be added but can't think of any right now

class HealthRecs(models.Model):
	health_profile = models.ForeignKey(HealthProfile,on_delete=models.CASCADE)
	doc = models.FileField(blank=True,null=True)
	view_perm=models.BooleanField()

class PreConsultation(models.Model):
	illness = models.CharField(max_length=50)
	desc = models.TextField()
	specialization = models.CharField(max_length=30)