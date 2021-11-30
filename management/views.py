from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from mailmeto.models import RequestImage
from .forms import ResponseForm
from django.contrib import messages
from .email_handler import send_confirmation_email


@login_required
def management(request):
    """
    Populates image response template
    """

    if not request.user.is_superuser:
        messages.error(request, 'Reserved for site operators.')
        return redirect(reverse('home'))

    requests = RequestImage.objects.all()

    context = {
        'requests': requests,
    }

    return render(request, 'management/management.html', context)

@login_required
def edit_request(request, ask_id):
    """
    Edit the request for an image
    """

    if not request.user.is_superuser:
        messages.error(request, 'Reserved for site operators.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        response_form = ResponseForm(request.POST)
        # save image request
        if response_form.is_valid():

            # display confirmation message
            messages.success(request,'Image request successfully processed! \
            A confirmation email will be sent to the subscriber')

            # send confirmation email
            image_response = {
                'request_name': response_form.cleaned_data['request_name'],
                'request_email': response_form.cleaned_data['request_email'],
                'description': response_form.cleaned_data['description'],
                'category': response_form.cleaned_data['category'],
                'site_owner_message': response_form.cleaned_data['site_owner_message'],
                'image': response_form.cleaned_data['image']
            }

            # Update the request
            RequestImage.objects.filter(id=ask_id).update(
                image=response_form.cleaned_data['image'],
                site_owner_message=response_form.cleaned_data['site_owner_message'] 
                )
            messages.success(request, 'Image request updated')

            delivered = True
            send_confirmation_email(image_response, delivered)
            return redirect(management)

        else:
            messages.error(request, 'Please complete the form correctly')

    else:
        request_for_image = get_object_or_404(RequestImage, id=ask_id)
        form = ResponseForm(instance=request_for_image)
    
    template = 'management/edit_request.html'

    context = {
        'form': form,
        'ask_id': ask_id
        }

    return render(request, template, context)


@login_required
def delete_request(request, ask_id):
    """
    Delete the request for an image
    """

    if not request.user.is_superuser:
        messages.error(request, 'Reserved for site operators.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        response_form = ResponseForm(request.POST)

        # delete image request 
        if response_form.is_valid():

            # send confirmation email
            image_response = {
                'request_name': response_form.cleaned_data['request_name'],
                'request_email': response_form.cleaned_data['request_email'],
                'description': response_form.cleaned_data['description'],
                'site_owner_message': response_form.cleaned_data['site_owner_message'],
                'category': response_form.cleaned_data['category']
            }
            delivered = False
            send_confirmation_email(image_response, delivered)

            # delete the image request
            image_request = get_object_or_404(RequestImage, pk=ask_id)
            image_request.delete()
            messages.success(request, 'Image request deleted')

            return redirect(management)
        else:
            messages.error(request, 'The image request has not been deleted.')

    else:
        request_for_image = get_object_or_404(RequestImage, id=ask_id)
        form = ResponseForm(instance=request_for_image)

    template = 'management/delete_request.html'

    context = {
        'form': form,
        'ask_id': ask_id,
        }

    return render(request, template, context)
