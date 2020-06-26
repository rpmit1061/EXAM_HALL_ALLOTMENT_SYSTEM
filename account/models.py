from django.db import models


# Create your models here.
class Destination(models.Model):
    username = models.CharField(max_length=100)
    password1 = models.CharField(max_length=32)
    password2 = models.CharField(max_length=32)
    mobile = models.CharField(max_length=100)
    dob = models.DateTimeField(max_length=100)

