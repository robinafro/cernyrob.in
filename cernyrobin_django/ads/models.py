from django.db import models

class Ad(models.Model):
    ad_id = models.AutoField(primary_key=True, auto_created=True)
    owner_name = models.CharField(max_length=30, null=False)
    name = models.CharField(max_length=30, default="ad")
    status = models.CharField(max_length=30, default="pending")
    image_link = models.CharField(max_length=100, null=False)
    link = models.CharField(max_length=100, default="")