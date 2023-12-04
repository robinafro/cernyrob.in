from django.db import models
from django.utils import timezone

class System(models.Model):
    key = models.CharField(max_length=20, unique=True)
    last_generated = models.IntegerField(default=0)

class Kafka(models.Model):
    video_url = models.CharField(max_length=70, unique=True)
    video_info = models.JSONField(default=dict)
    language = models.CharField(max_length=10)
    transcript = models.CharField(max_length=999999)
    answers = models.CharField(max_length=99999)
    timestamp = models.DateTimeField(auto_now_add=True)

class Job(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True)
    created = models.DateTimeField(default=timezone.now)
    video_url = models.CharField(max_length=70)
    percent_completed = models.IntegerField(default=0)
    chunks_completed = models.IntegerField(default=0)
    total_chunks = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)