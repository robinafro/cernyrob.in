from django.db import models

class System(models.Model):
    key = models.CharField(max_length=20, unique=True)
    last_generated = models.DateTimeField()

class Kafka(models.Model):
    video_url = models.CharField(max_length=70, unique=True)
    language = models.CharField(max_length=10)
    transcript = models.CharField(max_length=999999)
    answers = models.CharField(max_length=99999)
    timestamp = models.DateTimeField(auto_now_add=True)