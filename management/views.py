from django.shortcuts import render, get_object_or_404, redirect
from mailmeto.models import RequestImage
from .forms import ResponseForm
from django.contrib import messages
from .email_handler import send_confirmation_email


def management(request):
    """
    Populates image response template
    """
    requests = RequestImage.objects.all()

    context = {
        'requests': requests,
    }

    return render(request, 'management/management.html', context)


def edit_request(request, ask_id):
    """
    Edit the request for an image
    """

    if request.method == 'POST':
        response_form = ResponseForm(request.POST)
        # save image request
        if response_form.is_valid():
            response_form.save()

            # display confirmation message 
            messages.success(request, f'Image request successfully processed! \
            A confirmation email will be sent to the subscriber')

            # send confirmation email
            image_response = {
                'request_name': response_form.cleaned_data['request_name'],
                'request_email': response_form.cleaned_data['request_email'],
                'description': response_form.cleaned_data['description'],
                'category': response_form.cleaned_data['category'],
                'image': response_form.cleaned_data['image']
            }
            delivered = True
            send_confirmation_email(image_response, delivered)
            return redirect(management)

        else:
            messages.error(request, f'Please complete the form correctly')

    else:
        request_for_image = get_object_or_404(RequestImage, id=ask_id)
        form = ResponseForm(instance=request_for_image)
    
    template = 'management/edit_request.html'

    context = {
        'form': form,
        'ask_id': ask_id
        }

    return render(request, template, context)
    


def delete_request(request, ask_id):
    """
    Delete the request for an image
    """

    if request.method == 'POST':
        response_form = ResponseForm(request.POST)
        # delete image request 
        if response_form.is_valid():

            # send confirmation email
            image_response = {
                'request_name': response_form.cleaned_data['request_name'],
                'request_email': response_form.cleaned_data['request_email'],
                'description': response_form.cleaned_data['description'],
                'category': response_form.cleaned_data['category']
            }
            delivered = False
            send_confirmation_email(image_response, delivered)

            RequestImage.objects.filter(id=ask_id).delete()
            #send_confirmation_email(image_response)

            return redirect(management)
        else:
            messages.error(request, f'The image request has not been deleted.')
    
    else:
        request_for_image = get_object_or_404(RequestImage, id=ask_id)
        form = ResponseForm(instance=request_for_image)
        
    template = 'management/delete_request.html'

    context = {
        'form': form,
        'ask_id': ask_id,
        }

    return render(request, template, context)
