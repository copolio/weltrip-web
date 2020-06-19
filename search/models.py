from django.db import models

# Create your models here.

class SearchMeta(models.Model):
    key = models.CharField(max_length=20)
    user = models.CharField(max_length=20, default='anonymous')
    date = models.DateTimeField('date when the searching request is submitted')


class ClickDetail(models.Model):
    contentId = models.CharField(max_length=20)
    contentName = models.CharField(max_length=40)
    userId = models.CharField(max_length=20, default='anonymous')
    userType = models.CharField(max_length=20, default='NA')
    cat1 = models.CharField(max_length=20)
    cat2 = models.CharField(max_length=20)
    cat3 = models.CharField(max_length=20)
    date = models.DateTimeField('date')

    


class SearchObj(models.Model):
    key = models.CharField(max_length=20)
    content = models.TextField()
    


