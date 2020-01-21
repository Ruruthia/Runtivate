from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.IntegerField(default=0)
    height=models.IntegerField(default=0)
    age=models.IntegerField(default=0)
    gender=models.CharField(default='U', max_length=20)

class Activity(models.Model):

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE,)
    date = models.DateField()
    duration = models.IntegerField()
    distance = models.FloatField()
    comment = models.CharField(max_length=120)

