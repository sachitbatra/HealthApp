from django.db import models
import uuid
import datetime

class UserModel(models.Model):
    name = models.CharField(max_length=255)
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=4096)
    age = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

class SessionToken(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def create_token(self):
        self.session_token = uuid.uuid4()