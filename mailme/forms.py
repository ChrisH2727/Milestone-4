from django import forms
from .models import Request_image


class RequestForm(forms.ModelForm):
    """
    Sets up the image request form
    """

    class Meta:
        model = Request_image
        fields = ('request_name', 'request_email', 'category', 'description',)
