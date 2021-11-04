from django.db import models
from django.conf import settings
from images.models import Category


class RequestImage(models.Model):
    """
    Provides a user requested image
    """
    request_number = models.CharField(
        max_length=32, null=False, editable=False, default=1)
    category = models.ForeignKey(
        'images.Category', null=True, blank=True, on_delete=models.SET_NULL)
    request_name = models.CharField(max_length=50, null=False, blank=False)
    request_email = models.EmailField(max_length=254, null=False, blank=False)   
    description = models.CharField(max_length=25, null=False, blank=False)
    request_date = models.DateTimeField(auto_now_add=True)
    availability_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True)