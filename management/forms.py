from django import forms
from mailmeto.models import RequestImage


class ResponseForm(forms.ModelForm):
    """
    Sets up the image reponseform
    """

    class Meta:
        model = RequestImage
        fields = (
            'id',
            'request_name',
            'request_email',
            'category',
            'description',
            'image',
            )