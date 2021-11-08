from django import forms
from images.models import Image


class ImageManagementForm(forms.ModelForm):
    """
    Sets up form for adding, editing and deleteing an image
    (image inventory management)
    """

    class Meta:
        model = Image
        fields = (
            'category',
            'sku',
            'name',
            'size',
            'dimensions',
            'price',
            'views',
            'downloads',
            'image',
            )
