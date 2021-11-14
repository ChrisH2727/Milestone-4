from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserCredits(models.Model):
    """
    A user profile model for maintaining default
    customer information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credits = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class UserImages(models.Model):
    """
    Images historically downloaded by the user 
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    images_purchased = models.CharField(max_length=254, null=True, blank=True)
    def __str__(self):
        return self.user.username


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    customer information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
