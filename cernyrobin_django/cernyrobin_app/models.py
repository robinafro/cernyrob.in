from django.db import models

class ClickCount(models.Model):
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return str(self.count)