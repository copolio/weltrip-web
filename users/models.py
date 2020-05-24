from django.db import models
from django import forms
from django.contrib.auth.models import User
from PIL import Image
from multiselectfield import MultiSelectField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #CASCADE -> user가 deleted되면 profile도 delete 하라
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    disability_types = (
        ('PD', '지체 장애'),
        ('VD', '시각 장애'),
        ('AD', '청각 장애'),
        ('W/B', '영유아 동반'),
        ('NO', '해당 없음'),
    )
    disability = MultiSelectField(null=True, choices = disability_types)
    disability.verbose_name = "장애 유형"
    
    preference_types = (
        ('A0101', '자연관광지'),
        ('A0102', '관광자원'),
        ('A0201', '역사관광지'),
        ('A0202', '휴양관광지'),
        ('A0203', '체험관광지'),
        ('A0204', '산업관광지'),
        ('A0205', '건축/조형물'),
        ('A0206', '문화시설'),
        ('A0207', '축제'),
        ('A0208', '공연/행사'),
    )
    preference = MultiSelectField(null=True, choices = preference_types)
    preference.verbose_name = "선호 유형"

    def __str__(self):
        return f'{self.user.username} 님의 프로필'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path) # current instance의 image open

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)