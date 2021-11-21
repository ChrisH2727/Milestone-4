from django.shortcuts import render, redirect, get_object_or_404
from images.models import Category
from .forms import RequestForm
from .models import RequestImage
from django.views.decorators.http import require_POST
from django.contrib import messages
from .email_handler import send_confirmation_email
from django.contrib.auth.decorators import login_required


@login_required
def image_request(request):
    """
    Populates image request template
    """
    # get the request number associated with the last request or initialise
    if RequestImage.objects.filter(request_number=0).exists():
        latest_request = RequestImage.objects.last()
        last_request_number = latest_request.request_number
    else:
        last_request_number = 0

    # Proccess the new request     
    request_form = RequestForm()
    if request.method == 'POST':
        form = RequestForm(request.POST or None)

        # save image request 
        if form.is_valid():
            form.save()

            request_name = form.cleaned_data['request_name']
            request_email = form.cleaned_data['request_email']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']

            # display confirmation message 
            messages.success(request, f'A confirmation email will be sent to {request_email}.')

            # Update the request number
            new_request = RequestImage.objects.last()
            new_request.request_number = last_request_number + 1
            new_request.save()

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

