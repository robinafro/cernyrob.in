from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    clicks = models.IntegerField(default=0)
    clicks_auto = models.IntegerField(default=0)
    clicks_mult = models.IntegerField(default=0)

    phone_number = models.CharField(max_length=20, default="")