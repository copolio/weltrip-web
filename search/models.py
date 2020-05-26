from django.db import models

# Create your models here.

class SearchMeta(models.Model):
    key = models.CharField(max_length=20)
    user = models.CharField(max_length=20, default='anonymous')
    date = models.DateTimeField('date when the searching request is submitted')


class SearchObj(models.Model):
    key = models.CharField(max_length=20)
    content = models.TextField()
    


