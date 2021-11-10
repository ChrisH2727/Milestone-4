from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order
from pprint import pprint
from django.shortcuts import get_object_or_404


def send_order_confirmation_email(order_response):
    """Send the user a response email"""

    cust_email = order_response['email']

    subject = render_to_string(
        'pricing/confirmation_email/confirmation_email_subject.txt')

    body = render_to_string(
        'pricing/confirmation_email/confirmation_email_body.txt',
        {'order_response': order_response,
        'contact_email': settings.DEFAULT_FROM_EMAIL
        })

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email]
    )
    return
