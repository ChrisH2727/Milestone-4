from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name',
            'company_name',
            'address_line_1',
            'address_line_2',
            'town_or_city',
            'county',
            'postcode',
            'country',
            'email',
            )

