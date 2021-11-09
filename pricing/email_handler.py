from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_order_confirmation_email(order_response):
    """Send the user a response email"""
    cust_email = image_response['request_email']

    subject = render_to_string(
        'pricing/confirmation_email/response_email_subject.txt')

    body = render_to_string(
        'pricing/confirmation_email/response_email_body.txt',
        {'image_response': order_response,
        'contact_email': settings.DEFAULT_FROM_EMAIL
        })

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email]
    )
    return
