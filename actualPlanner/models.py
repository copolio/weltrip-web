import datetime

from django.db import models
from django.utils import timezone

class Planner(models.Model):
    date = models.DateTimeField('date last modified')
    user = models.CharField(max_length=20)
    title = models.CharField(max_length=30, default='새 일정')
    contents = models.TextField()
    rating = models.BooleanField(default=False)

    def __str__(self):
        return self.contents

    def was_date(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)

class Rating(models.Model):
    contentId = models.CharField(max_length=10)
    contentName = models.CharField(max_length=30)
    contentType = models.CharField(max_length=10)
    userRated = models.CharField(max_length=20)
    userDType = models.CharField(max_length=10)
    userPType = models.CharField(max_length=10, null=True)
    grade = models.IntegerField()

    def __str__(self):
        return "user_id: {}, contentName: {}, rating: {}, userDType: {}, userPType:{}"\
            .format(self.userRated, self.contentName, self.grade, self.userDType, self.userPType)
