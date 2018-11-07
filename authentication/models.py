from django.db import models
import uuid
import datetime

class UserModel(models.Model):
    name = models.CharField(max_length=255)
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=4096)
    dateOfBirth = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name
    @property
    def age(self):
        today = datetime.date.today()
        return today.year - self.dateOfBirth.year - ((today.month, today.day) < (self.dateOfBirth.month, self.dateOfBirth.day))

class DoctorModel(models.Model):
    name = models.CharField(max_length=255)
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=4096)
    dateOfBirth = models.DateTimeField(default=datetime.datetime.now)
    created_on = models.DateTimeField(auto_now_add=True)
    specialization = models.CharField(max_length=255)
    auth_document = models.FileField(upload_to='authenticationDocs')
    auth_document_url = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    experience = models.IntegerField()
    verified = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

class UserSessionToken(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def create_token(self):
        self.session_token = uuid.uuid4()

class DoctorSessionToken(models.Model):
    doctor = models.ForeignKey(DoctorModel, on_delete=models.CASCADE)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def create_token(self):
        self.session_token = uuid.uuid4()