from django.db import models
import uuid
import datetime


class AppUser(models.Model):
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
        return today.year - self.dateOfBirth.year - (
                    (today.month, today.day) < (self.dateOfBirth.month, self.dateOfBirth.day))


class GoogleCredentials(models.Model):
    user = models.ForeignKey(AppUser, primary_key=True, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    token_uri = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    scopes = models.CharField(max_length=1000)


class UserModel(AppUser):
    pass


class DoctorModel(AppUser):
    specialization = models.CharField(max_length=255)
    auth_document = models.FileField(upload_to='authenticationDocs')
    auth_document_url = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    experience = models.IntegerField()
    verified = models.BooleanField(default=False)


class UserSessionToken(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def create_token(self):
        self.session_token = uuid.uuid4()


class DoctorSessionToken(models.Model):
    user = models.ForeignKey(DoctorModel, on_delete=models.CASCADE)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def create_token(self):
        self.session_token = uuid.uuid4()
