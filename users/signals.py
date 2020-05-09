from django.db.models.signals import post_save
# DB model과 관련된 save 작동시 지정 동작 수행하는 signal
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# user 생성시 profile 자동 생성

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance) # user가 생성된 instance인 그 user


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
