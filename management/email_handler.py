from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from mailmeto.models import RequestImage

def send_confirmation_email(image_response, delivered):
    """Send the user a response email"""
    cust_email = image_response['request_email']

    subject = render_to_string(
        'management/confirmation_email/response_email_subject.txt')

    if delivered:
        body = render_to_string(
            'management/confirmation_email/response_email_body.txt',
            {'image_response': image_response,
            'contact_email': settings.DEFAULT_FROM_EMAIL
            })

    else:
        body = render_to_string(
            'management/confirmation_email/decline_email_body.txt',
            {'image_response': image_response,
            'contact_email': settings.DEFAULT_FROM_EMAIL
            })



    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email]
    )
    return