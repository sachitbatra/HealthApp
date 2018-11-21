from django.db import models
from authentication.models import UserModel
# Create your models here.

class Schedule(models.Model):

    user= models.ForeignKey(UserModel,on_delete=models.CASCADE)
    name = models.CharField(max_length = 100,default = "untitled")
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    # day = models.CharField(max_length = 15,default = "Monday")

    def __str__(self):
        return self.user + ":" + self.starttime + ":" + self.endtime + ":" + self.day

    # class Meta:
    #     unique_together = ('user','day',)

class Exercise(models.Model):
    #rtn = models.ForeignKey(Routines,on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    mg = models.CharField(max_length = 100)
    def __str__(self):
        return self.name

class Routines(models.Model):
    #dflt = Exercise(name='none',mg='none')
    schd = models.ForeignKey(Schedule,on_delete = models.CASCADE)
    exc = models.ForeignKey(Exercise,on_delete = models.CASCADE)
    reps = models.IntegerField()
    sets = models.IntegerField()

    def __str__(self):
        return self.reps + ":" + self.sets + ":" + self.schd
