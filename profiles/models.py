from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    customer information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=120, null=True, blank=True)
    address_line_1 = models.CharField(max_length=80, null=True, blank=True)
    address_line_2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    country = CountryField(blank_label='Country', null=True, blank=True)
    credits = models.PositiveIntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=40, null=True, blank=True)
    mobile_phone_number = models.CharField(max_length=40, null=True, blank=True)
    # phone_number = PhoneNumberField(unique = True, null = False, blank = False)
    # mobile_phone_number = PhoneNumberField(unique = True, null = False, blank = False)
    is_registered = models.BooleanField(default=False)

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

class UserImages(models.Model):
    """
    A user profile model for maintaining default
    customer information
    """
    user = models.ForeignKey(
        'UserProfile', null=True, blank=True, on_delete=models.SET_NULL)
    images_purchased = models.CharField(max_length=250, null=True, blank=True)
    username = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.images_purchased
