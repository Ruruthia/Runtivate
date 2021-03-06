from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    """Model used for representing user's profile with additional data required to counting burned calories."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    gender = models.CharField(default='U', max_length=20)


class Activity(models.Model):

    """Model used for representing an activity."""
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, )
    date = models.DateField()
    duration = models.IntegerField()
    distance = models.FloatField()
    comment = models.CharField(max_length=120)

    # For tests:

    def __str__(self):
        return self.comment
