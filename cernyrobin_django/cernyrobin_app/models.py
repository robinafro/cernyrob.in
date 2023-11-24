from django.contrib.auth.models import User
from django.db import models


class BaseUserProfile(models.Model):
    robin_clicker = {
        "clicks": 0,
        "clicks_auto": 0,
        "clicks_mult": 1,
    }

    callme = {
        "phone_number": models.CharField(max_length=20, default=""),
    }

    class Meta:
        abstract = True

class UserProfile(BaseUserProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class AnonymousUserProfile(BaseUserProfile):
    session_key = models.CharField(max_length=40, primary_key=True)