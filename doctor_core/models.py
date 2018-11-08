from django.db import models
from django.db.models import Avg,Count
from django.core.validators import MaxValueValidator, MinValueValidator

from authentication.models import UserModel,DoctorModel
# Create your models here.

class DoctorProfile(models.Model):
    user = models.OneToOneField(
        'authentication.DoctorModel', on_delete=models.CASCADE
    )
    bio = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, height_field="height_field", width_field="width_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    phone_no = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.user.name

    def __unicode__(self):
        return self.user.name

    @property
    def avg_rating(self):
        return FeedBack.objects.filter(consultation__doctor_id=self.user.id).aggregate(Avg('overall_rating'))


class Consultation(models.Model):
    doctor = models.ForeignKey(DoctorModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    no_days = models.IntegerField(default=3,validators=[MaxValueValidator(5), MinValueValidator(3)])
    created_on = models.DateTimeField(auto_now_add=True)
    diagnosis = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.doctor.name + "-" + self.user.name

    def __unicode__(self):
        return self.doctor.name + "-" + self.user.name

    #postconsultation = models.ForeignKey(PostConsultation,on_delete=models.CASCADE)


class FeedBack(models.Model):
    feedback = models.TextField(blank=True)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    overall_rating = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)]
    )
    quickness = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)]
    )
    treatment = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)]
    )

    def __str__(self):
        return self.consultation




