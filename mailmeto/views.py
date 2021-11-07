from django.shortcuts import render, redirect, get_object_or_404
from images.models import Category
from .forms import RequestForm
from .models import RequestImage
from django.views.decorators.http import require_POST
from django.contrib import messages
from .email_handler import send_confirmation_email

def image_request(request):
    """
    Populates image request template
    """
    request_form = RequestForm()
    if request.method == 'POST':
        form = RequestForm(request.POST or None)
        print("post mailmeto")
        # save image request 
        if form.is_valid():
            request_name = form.cleaned_data['request_name']
            request_email = form.cleaned_data['request_email']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            image = RequestImage(
                request_name=request_name,
                request_email=request_email,
                description=description,
                category=category
                )
            image.save()

            # display confirmation message 
            messages.success(request, f'Image request successfully processed! \
            A confirmation email will be sent to {request_email}.')

            # send confirmation email
            image_response = {
                'request_name': request_name,
                'request_email': request_email,
                'description': description,
                'category': category
            }
            send_confirmation_email(image_response)

            return render(request, 'mailmeto/mailme_success.html')
    else:
        context = {
            'request_form': request_form,
        }

    return render(request, 'mailmeto/mailme.html', context)

