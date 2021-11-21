from django import forms
from .models import RequestImage


class RequestForm(forms.ModelForm):
    """
    Sets up the image reponseform
    """

    class Meta:
        model = RequestImage
        exclude = ('request_number',
                    'request_date',
                    'availability_date',
                    'image',
                    'site_owner_message',
                    )
