from django.contrib.auth.models import User
from django.db import models
import json

class BaseUserProfile(models.Model):
    def get_default_robin_clicker():
        return {
            "clicks": 0,
            "clicks_auto": 0,
            "clicks_mult": 1,
        }

    def get_default_callme():
        return {
            "phone_number": "",
        }

    robin_clicker = models.CharField(max_length=100, default=json.dumps(get_default_robin_clicker()))

    callme = models.CharField(max_length=100, default=json.dumps(get_default_callme()))

    email_verified = models.BooleanField(default=False)
    email = models.CharField(max_length=100, default="")

    def __str__(self):
        return str(self.user)

    class Meta:
        abstract = True

    def get_robin_clicker(self):
        return json.loads(self.robin_clicker)

    def set_robin_clicker(self, value):
        self.robin_clicker = json.dumps(value)

    def get_callme(self):
        return json.loads(self.callme)
    
    def set_callme(self, value):
        self.callme = json.dumps(value)

class UserProfile(BaseUserProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class AnonymousUserProfile(BaseUserProfile):
    session_key = models.CharField(max_length=40, primary_key=True)