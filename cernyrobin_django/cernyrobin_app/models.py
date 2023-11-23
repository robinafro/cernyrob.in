from django.contrib.auth.models import User
from django.db import models


class BaseUserProfile(models.Model):
    clicks = models.IntegerField(default=0)
    clicks_auto = models.IntegerField(default=0)
    clicks_mult = models.IntegerField(default=1)

    phone_number = models.CharField(max_length=20, default="")

    class Meta:
        abstract = True

class UserProfile(BaseUserProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class AnonymousUserProfile(BaseUserProfile):
    session_key = models.CharField(max_length=40, primary_key=True)