from django.db import models
from django.utils import timezone

class System(models.Model):
    key = models.CharField(max_length=20, unique=True)
    last_generated = models.FloatField(default=0)

class Kafka(models.Model):
    video_url = models.CharField(max_length=70, unique=True, primary_key=True)
    video_info = models.JSONField(default=str)
    language = models.CharField(max_length=10, null=True)
    transcript = models.CharField(max_length=999999, null=True)
    answers = models.CharField(max_length=99999, null=True)
    timestamp = models.FloatField(default=0, null=True)

class Job(models.Model):
    job_id = models.CharField(max_length=20, unique=True, primary_key=True, default="")
    created = models.FloatField(default=0)
    video_url = models.CharField(max_length=700)
    percent_completed = models.IntegerField(default=0)
    chunks_completed = models.IntegerField(default=0)
    total_chunks = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)