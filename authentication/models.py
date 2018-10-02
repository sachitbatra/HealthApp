from django.db import models

class UserModel(models.Model):
    name = models.CharField(max_length=255)
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=4096)
    age = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
