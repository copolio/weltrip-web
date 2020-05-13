import datetime

from django.db import models
from django.utils import timezone

class Planner(models.Model):
    date = models.DateTimeField('date last modified')
    user = models.CharField(max_length=20)
    contents = models.TextField()

    def __str__(self):
        return self.contents

    def was_date(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)