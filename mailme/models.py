from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from images.models import Category
from profiles.models import UserProfile
import uuid


class Request_image(models.Model):
    """
    Provides a user requested image
    """
    request_number = models.CharField(
        max_length=32, null=False, editable=False)
    category = models.ForeignKey(
        'images.Category', null=True, blank=True, on_delete=models.SET_NULL)
    request_name = models.CharField(max_length=50, null=False, blank=False)
    request_email = models.EmailField(max_length=254, null=False, blank=False)   
    description = models.CharField(max_length=25, null=False, blank=False)
    request_date = models.DateTimeField(auto_now_add=True)
    availability_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True)


    def _generate_request_number(self):
        """
        Generate a random, unique request number using UUID
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the request number
        if it hasn't been set already.
        """

        if not self.request_number:
            self.request_number = self._generate_request_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.request_number
